FROM node:22-bookworm AS node

FROM python:3.12-bookworm AS python

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/code \
    PLAYWRIGHT_VERSION=1.58.2 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PNPM_HOME=/home/agent/.local/share/pnpm \
    PNPM_STORE_DIR=/home/agent/.local/share/pnpm/store \
    NPM_CONFIG_CACHE=/home/agent/.npm \
    XDG_DATA_HOME=/home/agent/.local/share \
    PATH=/home/agent/.local/share/pnpm:/usr/local/bin:${PATH}

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git curl wget ca-certificates gnupg lsb-release \
    unzip zip jq tree ripgrep fd-find tmux neovim vim shellcheck \
    pkg-config openssl sudo tini \
    openssh-server \
    chromium chromium-driver firefox-esr \
    xvfb xauth dbus dbus-x11 \
    fonts-liberation fonts-noto-color-emoji \
    postgresql-15 postgresql-client-15 postgresql-contrib-15 redis-tools \
    postgresql-15-postgis-3 postgresql-15-postgis-3-scripts \
    fzf zsh \
    && rm -rf /var/lib/apt/lists/*

# PX4 SITL + jMAVSim + demo-video toolchain (added for the MAV-GC PX4 work).
# - default-jdk + ant: build & run jMAVSim (the Java simulator PX4 talks to).
# - ffmpeg: x11grab capture of the jMAVSim 3D window for demo videos.
# - genromfs: PX4 SITL ROMFS image build step.
# - Mesa software GL (libgl1-mesa-dri / mesa-utils) lets jMAVSim's Java3D GUI
#   render under Xvfb (LIBGL_ALWAYS_SOFTWARE=1) without a real GPU.
# xvfb/xauth are already installed above; cmake/ninja come via pip (below) so we
# get a modern cmake (PX4 needs >= 3.x) without apt's older package.
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jdk ant \
    ffmpeg \
    genromfs \
    libgl1-mesa-dri mesa-utils \
    && rm -rf /var/lib/apt/lists/*

COPY --from=node /usr/local /usr/local

RUN groupadd agent \
    && useradd -m -g agent -s /bin/bash agent \
    && mkdir -p /code \
        /home/agent/.local/share/pnpm/store \
        /home/agent/.npm \
        /home/agent/.local/share \
        /var/run/sshd \
        /etc/ssh/sshd_config.d \
    && chown -R agent:agent /code /home/agent

RUN echo 'agent ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/agent \
    && chmod 0440 /etc/sudoers.d/agent

RUN npm install -g \
      pnpm@10 \
      playwright@${PLAYWRIGHT_VERSION} \
      @playwright/test@${PLAYWRIGHT_VERSION} \
    && pnpm config set store-dir "$PNPM_STORE_DIR" \
    && node --version \
    && npm --version \
    && pnpm --version \
    && playwright --version

RUN playwright install --with-deps chromium firefox webkit

RUN cat > /usr/local/bin/with-display <<'EOF_SCRIPT'
#!/bin/sh
exec xvfb-run -a --server-args="-screen 0 2560x1600x24" "$@"
EOF_SCRIPT

RUN chmod +x /usr/local/bin/with-display

RUN npm install -g \
      @openai/codex

ARG USER=agent
ARG HOME=/home/$USER

RUN chown -R agent:agent /home/agent /code

USER agent
WORKDIR /code

RUN pip install --no-cache-dir \
    selenium==4.41.0 \
    pytest==9.0.2 \
    pytest-cov==7.1.0 \
    pytest-xdist==3.8.0 \
    webdriver-manager==4.0.2

# PX4 SITL build/run toolchain + MAV-GC PX4 deps (installed into the agent
# user-site, like the block above). cmake/ninja here are the build system PX4's
# `make px4_sitl` invokes. The rest are PX4's Python build deps (Tools/setup/
# requirements.txt) — empy MUST stay < 4 (PX4's templates break on empy 4.x) —
# plus pymavlink (the Px4Adapter's MAVLink link) and matplotlib/pillow (demo
# ground-track plots + video-frame checks). The PX4 source itself is NOT in the
# image; it lives under resources/ (bind-mounted) and is built at run time — see
# docs/docker_environment.md.
RUN pip install --no-cache-dir \
    "cmake==4.3.2" "ninja==1.13.0" \
    "empy>=3.3,<4" future "jinja2>=2.8" jsonschema kconfiglib lark lxml \
    "numpy>=1.13" nunavut packaging pkgconfig psutil pycryptodome pygments \
    pymavlink pyros-genmsg pyserial "pyulog>=0.5.0" pyyaml requests \
    "six>=1.12.0" "sympy>=1.10.1" "toml>=0.9" cerberus coverage argcomplete \
    "matplotlib>=3.0" pillow

RUN curl -fsSL https://claude.ai/install.sh | bash

RUN echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

RUN npx --yes skills@1.4.6 add https://github.com/shadcn/ui \
      --skill shadcn \
      --agent codex \
      --agent claude-code \
      --global \
      --yes \
      --copy \
    && npx --yes skills@1.4.6 add https://github.com/vercel-labs/next-skills \
      --skill next-best-practices \
      --skill next-cache-components \
      --skill next-upgrade \
      --agent codex \
      --agent claude-code \
      --global \
      --yes \
      --copy \
    && npx --yes skills@1.4.6 add https://github.com/vercel-labs/next-browser \
      --skill next-browser \
      --agent codex \
      --agent claude-code \
      --global \
      --yes \
      --copy \
    && npx --yes skills@1.4.6 add https://github.com/wshobson/agents \
      --skill nodejs-backend-patterns \
      --agent codex \
      --agent claude-code \
      --global \
      --yes \
      --copy \
    && npx --yes skills@1.4.6 add https://github.com/supabase/agent-skills \
      --skill supabase-postgres-best-practices \
      --agent codex \
      --agent claude-code \
      --global \
      --yes \
      --copy \
    && npx --yes skills@1.4.6 add https://github.com/github/awesome-copilot \
      --skill postgresql-optimization \
      --agent codex \
      --agent claude-code \
      --global \
      --yes \
      --copy \
    && npx --yes skills@1.4.6 add https://github.com/github/awesome-copilot \
      --skill python-mcp-server-generator \
      --agent codex \
      --agent claude-code \
      --global \
      --yes \
      --copy \
    && npx --yes skills@1.4.6 add https://github.com/wshobson/agents \
      --skill python-testing-patterns \
      --agent codex \
      --agent claude-code \
      --global \
      --yes \
      --copy \
    && npx --yes skills@1.4.6 add https://github.com/wshobson/agents \
      --skill python-design-patterns \
      --agent codex \
      --agent claude-code \
      --global \
      --yes \
      --copy \
    && npx --yes skills@1.4.6 add https://github.com/wshobson/agents \
      --skill python-code-style \
      --agent codex \
      --agent claude-code \
      --global \
      --yes \
      --copy \
    && npx --yes skills@1.4.6 add https://github.com/wshobson/agents \
      --skill python-anti-patterns \
      --agent codex \
      --agent claude-code \
      --global \
      --yes \
      --copy

RUN echo `whoami`
RUN echo `groups`

USER root

RUN chown -R agent:agent /home/agent/.claude || true
RUN chown -R agent:agent /home/agent/.claude.json || true

RUN mkdir -p /home/agent/.ssh \
    && chown -R agent:agent /home/agent/.ssh \
    && chmod 700 /home/agent/.ssh \
    && ssh-keygen -A

RUN cat > /etc/ssh/sshd_config.d/10-agent.conf <<'EOF_SSH'
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
ChallengeResponseAuthentication no
PubkeyAuthentication yes
UsePAM yes
X11Forwarding yes
AllowUsers agent
AuthorizedKeysFile .ssh/authorized_keys
EOF_SSH

RUN cat > /usr/local/bin/container-init <<'EOF_SCRIPT'
#!/usr/bin/env bash
set -euo pipefail

ALLOW_SSH_PASSWORD="${ALLOW_SSH_PASSWORD:-false}"
AGENT_PASSWORD="${AGENT_PASSWORD:-}"
AUTHORIZED_KEYS="${AUTHORIZED_KEYS:-}"

install -d -m 700 -o agent -g agent /home/agent/.ssh

if [ -n "${AUTHORIZED_KEYS}" ]; then
  printf '%s\n' "${AUTHORIZED_KEYS}" > /home/agent/.ssh/authorized_keys
  chown agent:agent /home/agent/.ssh/authorized_keys
  chmod 600 /home/agent/.ssh/authorized_keys
fi

if [ "${ALLOW_SSH_PASSWORD}" = "true" ]; then
  if [ -z "${AGENT_PASSWORD}" ]; then
    echo "ALLOW_SSH_PASSWORD=true requires AGENT_PASSWORD to be set" >&2
    exit 1
  fi

  echo "agent:${AGENT_PASSWORD}" | chpasswd

  cat > /etc/ssh/sshd_config.d/20-auth-mode.conf <<'EOF_AUTH'
PasswordAuthentication yes
KbdInteractiveAuthentication yes
EOF_AUTH
else
  passwd -l agent >/dev/null

  cat > /etc/ssh/sshd_config.d/20-auth-mode.conf <<'EOF_AUTH'
PasswordAuthentication no
KbdInteractiveAuthentication no
EOF_AUTH
fi

/usr/sbin/sshd -e

cd /code
exec sudo -u agent -H /bin/bash -l
EOF_SCRIPT

RUN chmod +x /usr/local/bin/container-init

EXPOSE 22
EXPOSE 20522
EXPOSE 20523
EXPOSE 20524
EXPOSE 20525

ENV TINI_SUBREAPER=true
ENTRYPOINT ["/usr/bin/tini", "-s", "--", "/usr/local/bin/container-init"]
CMD ["/usr/local/bin/container-init"]
