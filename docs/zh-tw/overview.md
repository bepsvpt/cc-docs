> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code 概述

> Claude Code 是一個代理編碼工具，可以讀取您的程式碼庫、編輯檔案、執行命令，並與您的開發工具整合。可在您的終端機、IDE、桌面應用程式和瀏覽器中使用。

export const InstallConfigurator = ({defaultSurface = 'terminal'}) => {
  const TERM = {
    mac: {
      label: 'macOS / Linux',
      cmd: 'curl -fsSL https://claude.ai/install.sh | bash'
    },
    win: {
      label: 'Windows'
    },
    brew: {
      label: 'Homebrew',
      cmd: 'brew install --cask claude-code'
    },
    winget: {
      label: 'WinGet',
      cmd: 'winget install Anthropic.ClaudeCode'
    }
  };
  const WIN_VARIANTS = {
    ps: 'irm https://claude.ai/install.ps1 | iex',
    cmd: 'curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd'
  };
  const TABS = [{
    key: 'terminal',
    label: 'Terminal'
  }, {
    key: 'desktop',
    label: 'Desktop'
  }, {
    key: 'vscode',
    label: 'VS Code'
  }, {
    key: 'jetbrains',
    label: 'JetBrains'
  }];
  const ALT_TARGETS = {
    desktop: {
      name: 'Desktop',
      tagline: 'The full agent in a native app for macOS and Windows.',
      installLabel: 'Download the app',
      installHref: 'https://claude.com/download?utm_source=claude_code&utm_medium=docs&utm_content=configurator_desktop_download',
      guideHref: '/en/desktop-quickstart'
    },
    vscode: {
      name: 'VS Code',
      tagline: 'Review diffs, manage context, and chat without leaving your editor.',
      installLabel: 'Install from Marketplace',
      installHref: 'https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code',
      altCmd: 'code --install-extension anthropic.claude-code',
      guideHref: '/en/vs-code'
    },
    jetbrains: {
      name: 'JetBrains',
      tagline: 'Native plugin for IntelliJ, PyCharm, WebStorm, and other JetBrains IDEs.',
      installLabel: 'Install from Marketplace',
      installHref: 'https://plugins.jetbrains.com/plugin/27310-claude-code-beta-',
      guideHref: '/en/jetbrains'
    }
  };
  const PROVIDERS = [{
    key: 'anthropic',
    label: 'Anthropic'
  }, {
    key: 'bedrock',
    label: 'Amazon Bedrock'
  }, {
    key: 'foundry',
    label: 'Microsoft Foundry'
  }, {
    key: 'vertex',
    label: 'Google Vertex AI'
  }];
  const PROVIDER_NOTICE = {
    bedrock: <>
        <strong>Configure your AWS account first.</strong> Running on Bedrock
        requires model access enabled in the AWS console and IAM credentials.{' '}
        <a href="/en/amazon-bedrock">Bedrock setup guide →</a>
      </>,
    vertex: <>
        <strong>Configure your GCP project first.</strong> Running on Vertex AI
        requires the Vertex API enabled and a service account with the right
        permissions.{' '}
        <a href="/en/google-vertex-ai">Vertex setup guide →</a>
      </>,
    foundry: <>
        <strong>Configure your Azure resources first.</strong> Running on
        Microsoft Foundry requires an Azure subscription with a Foundry resource
        and model deployments provisioned.{' '}
        <a href="/en/microsoft-foundry">Foundry setup guide →</a>
      </>
  };
  const iconCheck = (size = 14) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <polyline points="20 6 9 17 4 12" />
    </svg>;
  const iconCopy = (size = 14) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="9" y="9" width="13" height="13" rx="2" />
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
    </svg>;
  const iconArrowRight = (size = 13) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>;
  const iconArrowUpRight = (size = 14) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="7" y1="17" x2="17" y2="7" />
      <polyline points="7 7 17 7 17 17" />
    </svg>;
  const iconInfo = (size = 16) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="16" x2="12" y2="12" />
      <line x1="12" y1="8" x2="12.01" y2="8" />
    </svg>;
  const [target, setTarget] = useState(defaultSurface);
  const [team, setTeam] = useState(false);
  const [provider, setProvider] = useState('anthropic');
  const [pkg, setPkg] = useState(() => (/Win/).test(navigator.userAgent) ? 'win' : 'mac');
  const [winCmd, setWinCmd] = useState(false);
  const [copied, setCopied] = useState(null);
  const copyTimer = useRef(null);
  const handleCopy = async (text, key) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      const ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    }
    clearTimeout(copyTimer.current);
    setCopied(key);
    copyTimer.current = setTimeout(() => setCopied(null), 1800);
  };
  const cardBodyCmd = (cmd, prompt) => {
    const on = copied === 'term';
    return <div className="cc-ic-card-body">
        <span className="cc-ic-prompt">{prompt || '$'}</span>
        <div className="cc-ic-cmd">{cmd}</div>
        <button type="button" className={'cc-ic-copy' + (on ? ' cc-ic-copied' : '')} onClick={() => handleCopy(cmd, 'term')}>
          {on ? iconCheck(13) : iconCopy(13)}
          <span>{on ? 'Copied' : 'Copy'}</span>
        </button>
      </div>;
  };
  const isWinInstaller = pkg === 'win';
  const isWinPrompt = pkg === 'win' || pkg === 'winget';
  const terminalCmd = isWinInstaller ? WIN_VARIANTS[winCmd ? 'cmd' : 'ps'] : TERM[pkg].cmd;
  const alt = ALT_TARGETS[target];
  const showNotice = team && provider !== 'anthropic';
  const STYLES = `
.cc-ic {
  --ic-slate: #141413;
  --ic-clay: #d97757;
  --ic-clay-deep: #c6613f;
  --ic-gray-000: #ffffff;
  --ic-gray-150: #f0eee6;
  --ic-gray-550: #73726c;
  --ic-gray-700: #3d3d3a;
  --ic-border-subtle: rgba(31, 30, 29, 0.08);
  --ic-border-default: rgba(31, 30, 29, 0.15);
  --ic-border-strong: rgba(31, 30, 29, 0.3);
  --ic-font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, 'Courier New', monospace;
  font-family: 'Anthropic Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 14px; line-height: 1.5; color: var(--ic-slate);
  margin: 8px 0 32px;
}
.dark .cc-ic {
  --ic-slate: #f0eee6;
  --ic-gray-000: #262624;
  --ic-gray-150: #1f1e1d;
  --ic-gray-550: #91908a;
  --ic-gray-700: #bfbdb4;
  --ic-border-subtle: rgba(240, 238, 230, 0.08);
  --ic-border-default: rgba(240, 238, 230, 0.14);
  --ic-border-strong: rgba(240, 238, 230, 0.28);
}
.dark .cc-ic-check { background: transparent; }
.dark .cc-ic-card { border: 0.5px solid var(--ic-border-subtle); }
.dark .cc-ic-p-pill.cc-ic-active { box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3); }
.cc-ic *, .cc-ic *::before, .cc-ic *::after { box-sizing: border-box; }
.cc-ic a { text-decoration: none; }
.cc-ic a:not([class]) { color: inherit; }
.cc-ic button { font-family: inherit; cursor: pointer; }

.cc-ic-tab-strip {
  display: inline-flex; gap: 2px;
  padding: 4px; background: var(--ic-gray-150);
  border-radius: 10px; overflow-x: auto;
  max-width: 100%;
}
.cc-ic-tab {
  appearance: none; background: none; border: none;
  padding: 10px 18px; font-size: 15px; font-weight: 430;
  color: var(--ic-gray-550); border-radius: 7px;
  white-space: nowrap;
  transition: color 0.12s, background-color 0.12s;
}
.cc-ic-tab:hover { color: var(--ic-gray-700); }
.cc-ic-tab.cc-ic-active {
  color: var(--ic-slate); font-weight: 500;
  background: var(--ic-gray-000);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
.dark .cc-ic-tab.cc-ic-active { box-shadow: 0 1px 3px rgba(0, 0, 0, 0.4); }

.cc-ic-team-wrap { padding: 16px 0 20px; }
.cc-ic-team-toggle {
  display: flex; align-items: center; gap: 12px; font-family: inherit;
  padding: 12px 16px; font-size: 14px; font-weight: 430;
  color: var(--ic-gray-700); cursor: pointer; user-select: none;
  width: fit-content; background: var(--ic-gray-150);
  border: 0.5px solid var(--ic-border-subtle); border-radius: 8px;
  transition: border-color 0.15s;
}
.cc-ic-team-toggle:hover { border-color: var(--ic-border-default); }
.cc-ic-team-toggle.cc-ic-checked {
  background: rgba(217, 119, 87, 0.08);
  border-color: rgba(217, 119, 87, 0.25);
}
.cc-ic-check {
  width: 16px; height: 16px;
  border: 1px solid var(--ic-border-strong); border-radius: 4px;
  background: var(--ic-gray-000);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.cc-ic-check svg { color: #fff; display: none; }
.cc-ic-team-toggle.cc-ic-checked .cc-ic-check { background: var(--ic-clay-deep); border-color: var(--ic-clay-deep); }
.cc-ic-team-toggle.cc-ic-checked .cc-ic-check svg { display: block; }

.cc-ic-team-reveal { display: flex; flex-direction: column; gap: 12px; margin-bottom: 16px; }
.cc-ic-sales {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; padding: 14px 16px;
  background: var(--ic-gray-000); border: 0.5px solid var(--ic-border-default);
  border-radius: 8px; flex-wrap: wrap;
}
.cc-ic-sales-text { font-size: 13px; color: var(--ic-gray-700); line-height: 1.5; flex: 1; min-width: 200px; }
.cc-ic-sales-text strong { font-weight: 550; color: var(--ic-slate); }
.cc-ic-sales-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.cc-ic-btn-clay {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--ic-clay-deep); color: #fff; border: none;
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
  transition: background-color 0.15s; white-space: nowrap;
}
.cc-ic-btn-clay:hover { background: var(--ic-clay); }
.cc-ic-btn-ghost {
  display: inline-flex; align-items: center; gap: 8px;
  background: transparent; color: var(--ic-gray-700);
  border: 0.5px solid var(--ic-border-default);
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
}
.cc-ic-btn-ghost:hover { background: rgba(0, 0, 0, 0.04); }

.cc-ic-provider-bar {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 16px; background: var(--ic-gray-150);
  border-radius: 8px; font-size: 13px; flex-wrap: wrap;
}
.cc-ic-provider-bar .cc-ic-label { color: var(--ic-gray-550); flex-shrink: 0; }
.cc-ic-provider-pills { display: flex; gap: 4px; flex-wrap: wrap; }
.cc-ic-p-pill {
  appearance: none; border: none; background: transparent;
  padding: 6px 12px; border-radius: 6px;
  font-size: 13px; font-weight: 430; color: var(--ic-gray-700);
  white-space: nowrap;
}
.cc-ic-p-pill:hover { background: rgba(0, 0, 0, 0.04); }
.cc-ic-p-pill.cc-ic-active {
  background: var(--ic-gray-000); color: var(--ic-slate);
  font-weight: 500; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
.cc-ic-provider-notice {
  display: flex; padding: 16px 18px;
  background: var(--ic-gray-000); border: 0.5px solid var(--ic-border-default);
  border-radius: 8px; gap: 14px; align-items: flex-start;
}
.cc-ic-provider-notice > svg { color: var(--ic-gray-550); margin-top: 2px; flex-shrink: 0; }
.cc-ic-provider-notice-body { font-size: 14px; line-height: 1.55; color: var(--ic-gray-700); }
.cc-ic-provider-notice-body strong { font-weight: 550; color: var(--ic-slate); }
.cc-ic-provider-notice-body a { color: var(--ic-clay-deep); font-weight: 500; }
.cc-ic-provider-notice-body a:hover { text-decoration: underline; }

.cc-ic-card { background: #141413; border-radius: 12px; overflow: hidden; }
.cc-ic-subtabs {
  display: flex; align-items: center;
  background: #1a1918;
  border-bottom: 0.5px solid rgba(255, 255, 255, 0.08);
  padding: 0 8px; overflow-x: auto;
}
.cc-ic-subtab {
  appearance: none; background: none; border: none;
  padding: 12px 16px; font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  position: relative; white-space: nowrap;
}
.cc-ic-subtab:hover { color: rgba(255, 255, 255, 0.75); }
.cc-ic-subtab.cc-ic-active { color: #fff; }
.cc-ic-subtab.cc-ic-active::after {
  content: ''; position: absolute;
  left: 12px; right: 12px; bottom: -0.5px;
  height: 2px; background: var(--ic-clay);
}
.cc-ic-shell-switch {
  display: inline-flex; gap: 2px;
  margin: 14px 26px 0; padding: 3px;
  background: rgba(255, 255, 255, 0.06);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  font-family: inherit;
}
.cc-ic-shell-option {
  font: inherit; font-size: 12px; font-weight: 500;
  padding: 5px 12px; border-radius: 6px;
  background: transparent; border: none;
  color: rgba(255, 255, 255, 0.55);
  cursor: pointer; user-select: none; white-space: nowrap;
  transition: color 120ms ease, background-color 120ms ease;
}
.cc-ic-shell-option:hover { color: rgba(255, 255, 255, 0.85); }
.cc-ic-shell-option.cc-ic-active {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.25);
}

.cc-ic-card-body { padding: 24px 26px; display: flex; align-items: flex-start; gap: 14px; }
.cc-ic-prompt {
  color: var(--ic-clay); font-family: var(--ic-font-mono);
  font-size: 17px; user-select: none; padding-top: 2px;
}
.cc-ic-cmd {
  flex: 1; font-family: var(--ic-font-mono);
  font-size: 17px; color: #f0eee6;
  line-height: 1.55; white-space: pre-wrap; word-break: break-word;
}
.cc-ic-copy {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(255, 255, 255, 0.08);
  border: 0.5px solid rgba(255, 255, 255, 0.12);
  color: rgba(255, 255, 255, 0.85);
  padding: 7px 13px; border-radius: 8px;
  font-size: 13px; font-weight: 500; flex-shrink: 0;
}
.cc-ic-copy:hover { background: rgba(255, 255, 255, 0.14); }
.cc-ic-copy.cc-ic-copied { background: var(--ic-clay-deep); border-color: var(--ic-clay-deep); color: #fff; }

.cc-ic-below {
  margin-top: 12px; font-size: 13px; color: var(--ic-gray-550);
  display: flex; gap: 16px; flex-wrap: wrap; align-items: baseline;
}
.cc-ic-below a { color: var(--ic-gray-700); border-bottom: 0.5px solid var(--ic-border-default); }
.cc-ic-below a:hover { color: var(--ic-clay-deep); border-bottom-color: var(--ic-clay-deep); }
.cc-ic-handoff {
  padding: 22px 24px;
  background: linear-gradient(180deg, #faf9f4 0%, #f3f1e9 100%);
  border: 0.5px solid var(--ic-border-default);
  border-radius: 12px;
  box-shadow: 0 1px 2px rgba(31, 30, 29, 0.04), 0 6px 16px -4px rgba(31, 30, 29, 0.06);
}
.dark .cc-ic-handoff {
  background: linear-gradient(180deg, #262624 0%, #1f1e1d 100%);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3), 0 6px 16px -4px rgba(0, 0, 0, 0.4);
}
.cc-ic-handoff-title {
  font-size: 16px; font-weight: 550; color: var(--ic-slate);
  letter-spacing: -0.01em; margin-bottom: 4px;
}
.cc-ic-handoff-sub {
  font-size: 14px; line-height: 1.5; color: var(--ic-gray-700);
  margin-bottom: 18px;
}
.cc-ic-handoff-actions { display: flex; gap: 10px; flex-wrap: wrap; }
.cc-ic-handoff-alt {
  margin-top: 12px; font-size: 12px; color: var(--ic-gray-550);
}
.cc-ic-handoff-alt code {
  font-family: var(--ic-font-mono); font-size: 11px;
  background: var(--ic-gray-150); padding: 2px 6px;
  border-radius: 4px; color: var(--ic-gray-700);
}
.cc-ic-copy-sm {
  appearance: none; border: none;
  display: inline-flex; align-items: center; justify-content: center;
  width: 22px; height: 22px;
  margin-left: 4px; vertical-align: middle;
  background: var(--ic-gray-150); color: var(--ic-gray-550);
  border-radius: 4px;
  transition: color 0.1s, background-color 0.1s;
}
.cc-ic-copy-sm:hover { color: var(--ic-gray-700); background: var(--ic-border-default); }
.cc-ic-copy-sm.cc-ic-copied { background: var(--ic-clay-deep); color: #fff; }

@media (max-width: 720px) {
  .cc-ic-tab { padding: 12px 14px; font-size: 14px; }
  .cc-ic-sales-actions { width: 100%; }
  .cc-ic-card-body { padding: 20px; }
  .cc-ic-cmd { font-size: 15px; }
}
`;
  return <div className="cc-ic not-prose">
      <style>{STYLES}</style>

      {}
      <div className="cc-ic-tab-strip" role="tablist">
        {TABS.map(t => <button key={t.key} type="button" role="tab" aria-selected={target === t.key} className={'cc-ic-tab' + (target === t.key ? ' cc-ic-active' : '')} onClick={() => setTarget(t.key)}>
            {t.label}
          </button>)}
      </div>

      {}
      <div className="cc-ic-team-wrap">
        <button type="button" role="switch" aria-checked={team} className={'cc-ic-team-toggle' + (team ? ' cc-ic-checked' : '')} onClick={() => setTeam(!team)}>
          <span className="cc-ic-check">{iconCheck(11)}</span>
          <span>
            I’m buying for a team or company (SSO, AWS/Azure/GCP, central billing)
          </span>
        </button>
      </div>

      {}
      {team && <div className="cc-ic-team-reveal">
          <div className="cc-ic-sales">
            <div className="cc-ic-sales-text">
              <strong>Set up your team:</strong> self-serve or talk to sales.
            </div>
            <div className="cc-ic-sales-actions">
              <a href="https://claude.ai/upgrade?initialPlanType=team&amp;utm_source=claude_code&amp;utm_medium=docs&amp;utm_content=configurator_team_get_started" className="cc-ic-btn-ghost">
                Get started
              </a>
              <a href="https://www.anthropic.com/contact-sales?utm_source=claude_code&amp;utm_medium=docs&amp;utm_content=configurator_team_contact_sales" className="cc-ic-btn-clay">
                Contact sales {iconArrowRight()}
              </a>
            </div>
          </div>

          <div className="cc-ic-provider-bar">
            <span className="cc-ic-label">Run on</span>
            <div className="cc-ic-provider-pills" role="radiogroup" aria-label="Provider">
              {PROVIDERS.map(p => <button key={p.key} type="button" role="radio" aria-checked={provider === p.key} className={'cc-ic-p-pill' + (provider === p.key ? ' cc-ic-active' : '')} onClick={() => setProvider(p.key)}>
                  {p.label}
                </button>)}
            </div>
          </div>

          {showNotice && <div className="cc-ic-provider-notice">
              {iconInfo()}
              <div className="cc-ic-provider-notice-body">
                {PROVIDER_NOTICE[provider]}
              </div>
            </div>}
        </div>}

      {}
      {target === 'terminal' && <div className="cc-ic-card">
          <div className="cc-ic-subtabs" role="tablist" aria-label="Install method">
            {Object.keys(TERM).map(k => <button key={k} type="button" role="tab" aria-selected={pkg === k} className={'cc-ic-subtab' + (pkg === k ? ' cc-ic-active' : '')} onClick={() => setPkg(k)}>
                {TERM[k].label}
              </button>)}
          </div>
          {isWinInstaller && <div className="cc-ic-shell-switch" role="tablist" aria-label="Shell">
              {[{
    k: 'ps',
    label: 'PowerShell'
  }, {
    k: 'cmd',
    label: 'CMD'
  }].map(({k, label}) => {
    const active = k === 'cmd' === winCmd;
    return <button key={k} type="button" role="tab" aria-selected={active} className={'cc-ic-shell-option' + (active ? ' cc-ic-active' : '')} onClick={() => setWinCmd(k === 'cmd')}>
                    {label}
                  </button>;
  })}
            </div>}
          {cardBodyCmd(terminalCmd, isWinPrompt ? '>' : '$')}
        </div>}

      {}
      {target === 'terminal' && <div className="cc-ic-below">
          {isWinInstaller && <span>
              <a href="https://git-scm.com/downloads/win" target="_blank" rel="noopener">
                Git for Windows
              </a>{' '}
              recommended. PowerShell is used if Git Bash is absent.
            </span>}
          {(pkg === 'brew' || pkg === 'winget') && <span>
              Does not auto-update. Run{' '}
              <code>{pkg === 'brew' ? 'brew upgrade claude-code' : 'winget upgrade Anthropic.ClaudeCode'}</code>{' '}
              periodically.
            </span>}
          <a href="/en/troubleshoot-install">Installation troubleshooting</a>
        </div>}

      {alt && <div className="cc-ic-handoff">
          <div className="cc-ic-handoff-title">Claude Code for {alt.name}</div>
          <div className="cc-ic-handoff-sub">{alt.tagline}</div>
          <div className="cc-ic-handoff-actions">
            <a href={alt.installHref} className="cc-ic-btn-clay" {...alt.installHref.startsWith('http') ? {
    target: '_blank',
    rel: 'noopener'
  } : {}}>
              {alt.installLabel} {iconArrowUpRight(13)}
            </a>
            <a href={alt.guideHref} className="cc-ic-btn-ghost">
              {alt.name} guide {iconArrowRight(12)}
            </a>
          </div>
          {alt.altCmd && <div className="cc-ic-handoff-alt">
              or run <code>{alt.altCmd}</code>
              <button type="button" className={'cc-ic-copy-sm' + (copied === 'alt' ? ' cc-ic-copied' : '')} onClick={() => handleCopy(alt.altCmd, 'alt')} aria-label="Copy command">
                {copied === 'alt' ? iconCheck(11) : iconCopy(11)}
              </button>
            </div>}
        </div>}
    </div>;
};

export const Experiment = ({flag, treatment, children}) => {
  const VID_KEY = 'exp_vid';
  const CONSENT_COUNTRIES = new Set(['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'RE', 'GP', 'MQ', 'GF', 'YT', 'BL', 'MF', 'PM', 'WF', 'PF', 'NC', 'AW', 'CW', 'SX', 'FO', 'GL', 'AX', 'GB', 'UK', 'AI', 'BM', 'IO', 'VG', 'KY', 'FK', 'GI', 'MS', 'PN', 'SH', 'TC', 'GG', 'JE', 'IM', 'CA', 'BR', 'IN']);
  const fnv1a = s => {
    let h = 0x811c9dc5;
    for (let i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h += (h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24);
    }
    return h >>> 0;
  };
  const bucket = (seed, vid) => fnv1a(fnv1a(seed + vid) + '') % 10000 < 5000 ? 'control' : 'treatment';
  const [decision] = useState(() => {
    const params = new URLSearchParams(location.search);
    const preBucketed = document.documentElement.dataset['gb_' + flag.replace(/-/g, '_')];
    const force = params.get('gb-force');
    if (force) {
      for (const p of force.split(',')) {
        const [k, v] = p.split(':');
        if (k === flag) return {
          variant: v || 'treatment',
          track: false
        };
      }
    }
    if (navigator.globalPrivacyControl) {
      return {
        variant: 'control',
        track: false
      };
    }
    const prefsMatch = document.cookie.match(/(?:^|; )anthropic-consent-preferences=([^;]+)/);
    if (prefsMatch) {
      try {
        if (JSON.parse(decodeURIComponent(prefsMatch[1])).analytics !== true) {
          return {
            variant: 'control',
            track: false
          };
        }
      } catch {
        return {
          variant: 'control',
          track: false
        };
      }
    } else {
      const country = params.get('country')?.toUpperCase() || (document.cookie.match(/(?:^|; )cf_geo=([A-Z]{2})/) || [])[1];
      if (!country || CONSENT_COUNTRIES.has(country)) {
        return {
          variant: 'control',
          track: false
        };
      }
    }
    let vid;
    try {
      const ajsMatch = document.cookie.match(/(?:^|; )ajs_anonymous_id=([^;]+)/);
      if (ajsMatch) {
        vid = decodeURIComponent(ajsMatch[1]).replace(/^"|"$/g, '');
      } else {
        vid = localStorage.getItem(VID_KEY);
        if (!vid) {
          vid = crypto.randomUUID();
        }
        document.cookie = `ajs_anonymous_id=${vid}; domain=.claude.com; path=/; Secure; SameSite=Lax; max-age=31536000`;
      }
      try {
        localStorage.setItem(VID_KEY, vid);
      } catch {}
    } catch {
      return {
        variant: 'control',
        track: false
      };
    }
    const variant = preBucketed === '1' ? 'treatment' : preBucketed === '0' ? 'control' : bucket(flag, vid);
    return {
      variant,
      track: true,
      vid
    };
  });
  useEffect(() => {
    if (!decision.track) return;
    fetch('https://api.anthropic.com/api/event_logging/v2/batch', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-service-name': 'claude_code_docs'
      },
      body: JSON.stringify({
        events: [{
          event_type: 'GrowthbookExperimentEvent',
          event_data: {
            device_id: decision.vid,
            anonymous_id: decision.vid,
            timestamp: new Date().toISOString(),
            experiment_id: flag,
            variation_id: decision.variant === 'treatment' ? 1 : 0,
            environment: 'production'
          }
        }]
      }),
      keepalive: true
    }).catch(() => {});
  }, []);
  return decision.variant === 'treatment' ? treatment : children;
};

Claude Code 是一個由 AI 驅動的編碼助手，可幫助您建立功能、修復錯誤和自動化開發任務。它理解您的整個程式碼庫，並可以跨多個檔案和工具工作以完成任務。

<div data-gb-slot="overview-install-configurator">
  <Experiment flag="overview-install-configurator" treatment={<InstallConfigurator />} />
</div>

## 開始使用

選擇您的環境以開始使用。大多數介面需要 [Claude 訂閱](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=overview_pricing)或 [Anthropic Console](https://console.anthropic.com/) 帳戶。終端機 CLI 和 VS Code 也支援[第三方提供商](/zh-TW/third-party-integrations)。

<Tabs>
  <Tab title="終端機">
    功能完整的 CLI，用於直接在您的終端機中使用 Claude Code。編輯檔案、執行命令，並從命令列管理您的整個專案。

    To install Claude Code, use one of the following methods:

    <Tabs>
      <Tab title="Native Install (Recommended)">
        **macOS, Linux, WSL:**

        ```bash theme={null}
        curl -fsSL https://claude.ai/install.sh | bash
        ```

        **Windows PowerShell:**

        ```powershell theme={null}
        irm https://claude.ai/install.ps1 | iex
        ```

        **Windows CMD:**

        ```batch theme={null}
        curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
        ```

        If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. If you see `'irm' is not recognized as an internal or external command`, you're in CMD, not PowerShell. Your prompt shows `PS C:\` when you're in PowerShell and `C:\` without the `PS` when you're in CMD.

        [Git for Windows](https://git-scm.com/downloads/win) is recommended on native Windows so Claude Code can use the Bash tool. If Git for Windows is not installed, Claude Code uses PowerShell as the shell tool instead. WSL setups do not need Git for Windows.

        <Info>
          Native installations automatically update in the background to keep you on the latest version.
        </Info>
      </Tab>

      <Tab title="Homebrew">
        ```bash theme={null}
        brew install --cask claude-code
        ```

        Homebrew offers two casks. `claude-code` tracks the stable release channel, which is typically about a week behind and skips releases with major regressions. `claude-code@latest` tracks the latest channel and receives new versions as soon as they ship.

        <Info>
          Homebrew installations do not auto-update. Run `brew upgrade claude-code` or `brew upgrade claude-code@latest`, depending on which cask you installed, to get the latest features and security fixes.
        </Info>
      </Tab>

      <Tab title="WinGet">
        ```powershell theme={null}
        winget install Anthropic.ClaudeCode
        ```

        <Info>
          WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
        </Info>
      </Tab>
    </Tabs>

    You can also install with [apt, dnf, or apk](/en/setup#install-with-linux-package-managers) on Debian, Fedora, RHEL, and Alpine.

    然後在任何專案中啟動 Claude Code：

    ```bash theme={null}
    cd your-project
    claude
    ```

    首次使用時，系統會提示您登入。就這麼簡單！[繼續進行快速入門 →](/zh-TW/quickstart)

    <Tip>
      請參閱[進階設定](/zh-TW/setup)以了解安裝選項、手動更新或卸載說明。如果遇到問題，請造訪[安裝疑難排解](/zh-TW/troubleshoot-install)。
    </Tip>
  </Tab>

  <Tab title="VS Code">
    VS Code 擴充功能在您的編輯器中直接提供內嵌差異、@-提及、計畫審查和對話歷史記錄。

    * [安裝 VS Code](vscode:extension/anthropic.claude-code)
    * [安裝 Cursor](cursor:extension/anthropic.claude-code)

    或在擴充功能檢視中搜尋「Claude Code」（Mac 上為 `Cmd+Shift+X`，Windows/Linux 上為 `Ctrl+Shift+X`）。安裝後，開啟命令選擇板（`Cmd+Shift+P` / `Ctrl+Shift+P`），輸入「Claude Code」，然後選擇**在新標籤中開啟**。

    [開始使用 VS Code →](/zh-TW/vs-code#get-started)
  </Tab>

  <Tab title="桌面應用程式">
    一個獨立應用程式，用於在 IDE 或終端機外執行 Claude Code。以視覺方式審查差異、並排執行多個工作階段、排程重複任務，以及啟動雲端工作階段。

    下載並安裝：

    * [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs)（Intel 和 Apple Silicon）
    * [Windows](https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs)（x64）
    * [Windows ARM64](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs)

    安裝後，啟動 Claude，登入，然後按一下**程式碼**標籤以開始編碼。需要[付費訂閱](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=overview_desktop_pricing)。

    [深入了解桌面應用程式 →](/zh-TW/desktop-quickstart)
  </Tab>

  <Tab title="網頁">
    在您的瀏覽器中執行 Claude Code，無需本機設定。啟動長時間執行的任務，並在完成時檢查，處理您本機沒有的儲存庫，或並行執行多個任務。可在桌面瀏覽器和 Claude iOS 應用程式上使用。

    在 [claude.ai/code](https://claude.ai/code) 開始編碼。

    [開始在網頁上使用 →](/zh-TW/web-quickstart)
  </Tab>

  <Tab title="JetBrains">
    IntelliJ IDEA、PyCharm、WebStorm 和其他 JetBrains IDE 的外掛程式，具有互動式差異檢視和選擇內容共享。

    從 JetBrains Marketplace 安裝 [Claude Code 外掛程式](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-)，然後重新啟動您的 IDE。

    [開始使用 JetBrains →](/zh-TW/jetbrains)
  </Tab>
</Tabs>

## 您可以做什麼

以下是您可以使用 Claude Code 的一些方式：

<AccordionGroup>
  <Accordion title="自動化您一直在推遲的工作" icon="wand-magic-sparkles">
    Claude Code 處理佔用您一整天的繁瑣任務：為未測試的程式碼編寫測試、修復整個專案中的 lint 錯誤、解決合併衝突、更新依賴項和編寫發行說明。

    ```bash theme={null}
    claude "write tests for the auth module, run them, and fix any failures"
    ```
  </Accordion>

  <Accordion title="建立功能和修復錯誤" icon="hammer">
    用純文字描述您想要的內容。Claude Code 規劃方法、跨多個檔案編寫程式碼，並驗證其是否有效。

    對於錯誤，貼上錯誤訊息或描述症狀。Claude Code 透過您的程式碼庫追蹤問題、識別根本原因並實施修復。請參閱[常見工作流程](/zh-TW/common-workflows)以了解更多範例。
  </Accordion>

  <Accordion title="建立提交和拉取請求" icon="code-branch">
    Claude Code 直接與 git 配合使用。它暫存變更、編寫提交訊息、建立分支並開啟拉取請求。

    ```bash theme={null}
    claude "commit my changes with a descriptive message"
    ```

    在 CI 中，您可以使用 [GitHub Actions](/zh-TW/github-actions) 或 [GitLab CI/CD](/zh-TW/gitlab-ci-cd) 自動化程式碼審查和問題分類。
  </Accordion>

  <Accordion title="使用 MCP 連接您的工具" icon="plug">
    [Model Context Protocol (MCP)](/zh-TW/mcp) 是一個開放標準，用於將 AI 工具連接到外部資料來源。使用 MCP，Claude Code 可以讀取 Google Drive 中的設計文件、更新 Jira 中的票證、從 Slack 提取資料，或使用您自己的自訂工具。
  </Accordion>

  <Accordion title="使用說明、skills 和 hooks 進行自訂" icon="sliders">
    [`CLAUDE.md`](/zh-TW/memory) 是您新增到專案根目錄的 markdown 檔案，Claude Code 在每個工作階段開始時都會讀取。使用它來設定編碼標準、架構決策、首選程式庫和審查檢查清單。Claude 也會在工作時建立[自動記憶](/zh-TW/memory#auto-memory)，儲存學習內容，例如建置命令和除錯見解，跨工作階段而無需您編寫任何內容。

    建立[自訂命令](/zh-TW/skills)以封裝您的團隊可以共享的可重複工作流程，例如 `/review-pr` 或 `/deploy-staging`。

    [Hooks](/zh-TW/hooks) 可讓您在 Claude Code 動作之前或之後執行 shell 命令，例如在每次檔案編輯後自動格式化或在提交前執行 lint。
  </Accordion>

  <Accordion title="執行代理團隊並建立自訂代理" icon="users">
    生成[多個 Claude Code 代理](/zh-TW/sub-agents)，同時處理任務的不同部分。主導代理協調工作、指派子任務並合併結果。

    對於完全自訂的工作流程，[Agent SDK](/zh-TW/agent-sdk/overview) 可讓您建立由 Claude Code 的工具和功能驅動的自己的代理，並完全控制編排、工具存取和權限。
  </Accordion>

  <Accordion title="使用 CLI 進行管道、指令碼和自動化" icon="terminal">
    Claude Code 是可組合的，遵循 Unix 哲學。將日誌管道傳入其中、在 CI 中執行它，或將其與其他工具鏈接：

    ```bash theme={null}
    # 分析最近的日誌輸出
    tail -200 app.log | claude -p "Slack me if you see any anomalies"

    # 在 CI 中自動化翻譯
    claude -p "translate new strings into French and raise a PR for review"

    # 跨檔案的大量操作
    git diff main --name-only | claude -p "review these changed files for security issues"
    ```

    請參閱 [CLI 參考](/zh-TW/cli-reference)以了解完整的命令和旗標集。
  </Accordion>

  <Accordion title="排程重複任務" icon="clock">
    按排程執行 Claude 以自動化重複的工作：早上 PR 審查、隔夜 CI 失敗分析、每週依賴項審計或在 PR 合併後同步文件。

    * [Routines](/zh-TW/routines) 在 Anthropic 管理的基礎設施上執行，因此即使您的電腦關閉，它們也會繼續執行。它們也可以在 API 呼叫或 GitHub 事件上觸發。從網頁、桌面應用程式或在 CLI 中執行 `/schedule` 來建立它們。
    * [桌面排程任務](/zh-TW/desktop-scheduled-tasks)在您的機器上執行，可直接存取您的本機檔案和工具
    * [`/loop`](/zh-TW/scheduled-tasks) 在 CLI 工作階段中重複提示以進行快速輪詢
  </Accordion>

  <Accordion title="從任何地方工作" icon="globe">
    工作階段不受限於單一介面。當您的內容變更時，在環境之間移動工作：

    * 離開您的辦公桌，使用[遠端控制](/zh-TW/remote-control)從您的手機或任何瀏覽器繼續工作
    * 從您的手機向 [Dispatch](/zh-TW/desktop#sessions-from-dispatch) 傳送任務，並開啟它建立的桌面工作階段
    * 在[網頁](/zh-TW/claude-code-on-the-web)或 [iOS 應用程式](https://apps.apple.com/app/claude-by-anthropic/id6473753684)上啟動長時間執行的任務，然後使用 `claude --teleport` 將其提取到您的終端機中
    * 使用 `/desktop` 將終端機工作階段交付給[桌面應用程式](/zh-TW/desktop)以進行視覺差異審查
    * 從團隊聊天路由任務：在 [Slack](/zh-TW/slack) 中提及 `@Claude` 並提供錯誤報告，然後取回拉取請求
  </Accordion>
</AccordionGroup>

## 在任何地方使用 Claude Code

每個介面都連接到相同的基礎 Claude Code 引擎，因此您的 CLAUDE.md 檔案、設定和 MCP servers 可在所有介面中工作。

除了上述[終端機](/zh-TW/quickstart)、[VS Code](/zh-TW/vs-code)、[JetBrains](/zh-TW/jetbrains)、[桌面](/zh-TW/desktop)和[網頁](/zh-TW/claude-code-on-the-web)環境外，Claude Code 還與 CI/CD、聊天和瀏覽器工作流程整合：

| 我想要...                                               | 最佳選項                                                                                                                |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| 從我的手機或其他裝置繼續本機工作階段                                   | [遠端控制](/zh-TW/remote-control)                                                                                       |
| 從 Telegram、Discord、iMessage 或我自己的 webhooks 推送事件到工作階段 | [Channels](/zh-TW/channels)                                                                                         |
| 在本機啟動任務，在行動裝置上繼續                                     | [網頁](/zh-TW/claude-code-on-the-web)或 [Claude iOS 應用程式](https://apps.apple.com/app/claude-by-anthropic/id6473753684) |
| 按重複排程執行 Claude                                       | [Routines](/zh-TW/routines) 或[桌面排程任務](/zh-TW/desktop-scheduled-tasks)                                               |
| 自動化 PR 審查和問題分類                                       | [GitHub Actions](/zh-TW/github-actions) 或 [GitLab CI/CD](/zh-TW/gitlab-ci-cd)                                       |
| 在每個 PR 上獲得自動程式碼審查                                    | [GitHub Code Review](/zh-TW/code-review)                                                                            |
| 將 Slack 中的錯誤報告路由到拉取請求                                | [Slack](/zh-TW/slack)                                                                                               |
| 除錯即時網頁應用程式                                           | [Chrome](/zh-TW/chrome)                                                                                             |
| 為您自己的工作流程建立自訂代理                                      | [Agent SDK](/zh-TW/agent-sdk/overview)                                                                              |

## 後續步驟

安裝 Claude Code 後，這些指南可幫助您深入了解。

* [快速入門](/zh-TW/quickstart)：逐步完成您的第一個真實任務，從探索程式碼庫到提交修復
* [儲存說明和記憶](/zh-TW/memory)：使用 CLAUDE.md 檔案和自動記憶為 Claude 提供持久說明
* [常見工作流程](/zh-TW/common-workflows)和[最佳實踐](/zh-TW/best-practices)：充分利用 Claude Code 的模式
* [設定](/zh-TW/settings)：為您的工作流程自訂 Claude Code
* [疑難排解](/zh-TW/troubleshooting)：常見問題的解決方案
* [code.claude.com](https://code.claude.com/)：演示、定價和產品詳細資訊
