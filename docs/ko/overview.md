> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code 개요

> Claude Code는 코드베이스를 읽고, 파일을 편집하고, 명령을 실행하고, 개발 도구와 통합하는 에이전트 코딩 도구입니다. 터미널, IDE, 데스크톱 앱 및 브라우저에서 사용할 수 있습니다.

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

Claude Code는 기능을 구축하고, 버그를 수정하고, 개발 작업을 자동화하는 데 도움이 되는 AI 기반 코딩 어시스턴트입니다. 전체 코드베이스를 이해하고 여러 파일과 도구에 걸쳐 작업할 수 있습니다.

<div data-gb-slot="overview-install-configurator">
  <Experiment flag="overview-install-configurator" treatment={<InstallConfigurator />} />
</div>

## 시작하기

환경을 선택하여 시작하세요. 대부분의 환경에는 [Claude 구독](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=overview_pricing) 또는 [Anthropic Console](https://console.anthropic.com/) 계정이 필요합니다. Terminal CLI 및 VS Code는 [타사 제공자](/ko/third-party-integrations)도 지원합니다.

<Tabs>
  <Tab title="Terminal">
    터미널에서 Claude Code로 직접 작업하기 위한 모든 기능을 갖춘 CLI입니다. 파일을 편집하고, 명령을 실행하고, 명령줄에서 전체 프로젝트를 관리할 수 있습니다.

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

    그런 다음 모든 프로젝트에서 Claude Code를 시작합니다:

    ```bash theme={null}
    cd your-project
    claude
    ```

    처음 사용할 때 로그인하라는 메시지가 표시됩니다. 이제 끝입니다! [빠른 시작으로 계속하기 →](/ko/quickstart)

    <Tip>
      [고급 설정](/ko/setup)에서 설치 옵션, 수동 업데이트 또는 제거 지침을 참조하세요. 문제가 발생하면 [설치 문제 해결](/ko/troubleshoot-install)을 방문하세요.
    </Tip>
  </Tab>

  <Tab title="VS Code">
    VS Code 확장 프로그램은 인라인 diff, @-mentions, 계획 검토 및 대화 기록을 편집기에서 직접 제공합니다.

    * [VS Code용 설치](vscode:extension/anthropic.claude-code)
    * [Cursor용 설치](cursor:extension/anthropic.claude-code)

    또는 확장 프로그램 보기(`Mac에서 Cmd+Shift+X`, `Windows/Linux에서 Ctrl+Shift+X`)에서 "Claude Code"를 검색합니다. 설치 후 명령 팔레트(`Cmd+Shift+P` / `Ctrl+Shift+P`)를 열고 "Claude Code"를 입력한 다음 **새 탭에서 열기**를 선택합니다.

    [VS Code 시작하기 →](/ko/vs-code#get-started)
  </Tab>

  <Tab title="Desktop app">
    IDE 또는 터미널 외부에서 Claude Code를 실행하기 위한 독립 실행형 앱입니다. diff를 시각적으로 검토하고, 여러 세션을 나란히 실행하고, 반복되는 작업을 예약하고, 클라우드 세션을 시작할 수 있습니다.

    다운로드 및 설치:

    * [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) (Intel 및 Apple Silicon)
    * [Windows](https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs) (x64)
    * [Windows ARM64](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs)

    설치 후 Claude를 실행하고, 로그인한 다음 **Code** 탭을 클릭하여 코딩을 시작합니다. [유료 구독](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=overview_desktop_pricing)이 필요합니다.

    [데스크톱 앱에 대해 자세히 알아보기 →](/ko/desktop-quickstart)
  </Tab>

  <Tab title="Web">
    로컬 설정 없이 브라우저에서 Claude Code를 실행합니다. 오래 실행되는 작업을 시작하고 완료되면 다시 확인하거나, 로컬에 없는 리포지토리에서 작업하거나, 여러 작업을 병렬로 실행할 수 있습니다. 데스크톱 브라우저 및 Claude iOS 앱에서 사용할 수 있습니다.

    [claude.ai/code](https://claude.ai/code)에서 코딩을 시작합니다.

    [웹에서 시작하기 →](/ko/web-quickstart)
  </Tab>

  <Tab title="JetBrains">
    IntelliJ IDEA, PyCharm, WebStorm 및 기타 JetBrains IDE용 플러그인으로 대화형 diff 보기 및 선택 컨텍스트 공유 기능이 있습니다.

    JetBrains Marketplace에서 [Claude Code 플러그인](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-)을 설치하고 IDE를 다시 시작합니다.

    [JetBrains 시작하기 →](/ko/jetbrains)
  </Tab>
</Tabs>

## 할 수 있는 것

Claude Code를 사용할 수 있는 몇 가지 방법은 다음과 같습니다:

<AccordionGroup>
  <Accordion title="계속 미루고 있는 작업 자동화" icon="wand-magic-sparkles">
    Claude Code는 하루를 낭비하는 지루한 작업을 처리합니다: 테스트되지 않은 코드에 대한 테스트 작성, 프로젝트 전체의 lint 오류 수정, 병합 충돌 해결, 종속성 업데이트 및 릴리스 노트 작성.

    ```bash theme={null}
    claude "write tests for the auth module, run them, and fix any failures"
    ```
  </Accordion>

  <Accordion title="기능 구축 및 버그 수정" icon="hammer">
    원하는 것을 일반 언어로 설명합니다. Claude Code는 접근 방식을 계획하고, 여러 파일에 걸쳐 코드를 작성하고, 작동하는지 확인합니다.

    버그의 경우 오류 메시지를 붙여넣거나 증상을 설명합니다. Claude Code는 코드베이스를 통해 문제를 추적하고, 근본 원인을 파악하고, 수정을 구현합니다. 더 많은 예제는 [일반적인 워크플로우](/ko/common-workflows)를 참조하세요.
  </Accordion>

  <Accordion title="커밋 및 풀 요청 생성" icon="code-branch">
    Claude Code는 git과 직접 작동합니다. 변경 사항을 스테이징하고, 커밋 메시지를 작성하고, 브랜치를 생성하고, 풀 요청을 엽니다.

    ```bash theme={null}
    claude "commit my changes with a descriptive message"
    ```

    CI에서 [GitHub Actions](/ko/github-actions) 또는 [GitLab CI/CD](/ko/gitlab-ci-cd)를 사용하여 코드 검토 및 이슈 분류를 자동화할 수 있습니다.
  </Accordion>

  <Accordion title="MCP로 도구 연결" icon="plug">
    [Model Context Protocol (MCP)](/ko/mcp)는 AI 도구를 외부 데이터 소스에 연결하기 위한 개방형 표준입니다. MCP를 사용하면 Claude Code는 Google Drive에서 설계 문서를 읽고, Jira에서 티켓을 업데이트하고, Slack에서 데이터를 가져오거나, 자신의 커스텀 도구를 사용할 수 있습니다.
  </Accordion>

  <Accordion title="지침, skills 및 hooks로 사용자 정의" icon="sliders">
    [`CLAUDE.md`](/ko/memory)는 프로젝트 루트에 추가하는 마크다운 파일로 Claude Code가 모든 세션의 시작 부분에서 읽습니다. 이를 사용하여 코딩 표준, 아키텍처 결정, 선호하는 라이브러리 및 검토 체크리스트를 설정합니다. Claude는 또한 작업할 때 [자동 메모리](/ko/memory#auto-memory)를 구축하여 빌드 명령 및 디버깅 인사이트와 같은 학습 내용을 저장하므로 아무것도 작성할 필요가 없습니다.

    [커스텀 명령](/ko/skills)을 생성하여 팀이 공유할 수 있는 반복 가능한 워크플로우를 패키징합니다(예: `/review-pr` 또는 `/deploy-staging`).

    [Hooks](/ko/hooks)를 사용하면 Claude Code 작업 전후에 셸 명령을 실행할 수 있습니다(예: 모든 파일 편집 후 자동 포맷팅 또는 커밋 전 lint 실행).
  </Accordion>

  <Accordion title="에이전트 팀 실행 및 커스텀 에이전트 구축" icon="users">
    작업의 다른 부분에서 동시에 작동하는 [여러 Claude Code 에이전트](/ko/sub-agents)를 생성합니다. 리드 에이전트가 작업을 조정하고, 하위 작업을 할당하고, 결과를 병합합니다.

    완전히 커스텀 워크플로우의 경우 [Agent SDK](/ko/agent-sdk/overview)를 사용하면 Claude Code의 도구 및 기능으로 구동되는 자신의 에이전트를 구축할 수 있으며, 오케스트레이션, 도구 액세스 및 권한에 대한 완전한 제어가 가능합니다.
  </Accordion>

  <Accordion title="CLI로 파이프, 스크립트 및 자동화" icon="terminal">
    Claude Code는 구성 가능하며 Unix 철학을 따릅니다. 로그를 파이프하고, CI에서 실행하거나, 다른 도구와 연결합니다:

    ```bash theme={null}
    # 최근 로그 출력 분석
    tail -200 app.log | claude -p "Slack me if you see any anomalies"

    # CI에서 번역 자동화
    claude -p "translate new strings into French and raise a PR for review"

    # 파일 전체에 걸친 대량 작업
    git diff main --name-only | claude -p "review these changed files for security issues"
    ```

    전체 명령 및 플래그 세트는 [CLI 참조](/ko/cli-reference)를 참조하세요.
  </Accordion>

  <Accordion title="반복되는 작업 예약" icon="clock">
    Claude를 일정에 따라 실행하여 반복되는 작업을 자동화합니다: 아침 PR 검토, 야간 CI 실패 분석, 주간 종속성 감사 또는 PR 병합 후 문서 동기화.

    * [Routines](/ko/routines)는 Anthropic 관리 인프라에서 실행되므로 컴퓨터가 꺼져 있어도 계속 실행됩니다. API 호출 또는 GitHub 이벤트에서도 트리거될 수 있습니다. 웹, 데스크톱 앱에서 생성하거나 CLI에서 `/schedule`을 실행하여 생성합니다.
    * [데스크톱 예약된 작업](/ko/desktop-scheduled-tasks)은 머신에서 실행되며 로컬 파일 및 도구에 직접 액세스할 수 있습니다
    * [`/loop`](/ko/scheduled-tasks)는 빠른 폴링을 위해 CLI 세션 내에서 프롬프트를 반복합니다
  </Accordion>

  <Accordion title="어디서나 작업" icon="globe">
    세션은 단일 환경에 연결되지 않습니다. 컨텍스트가 변경되면 환경 간에 작업을 이동합니다:

    * 책상에서 떠나 [원격 제어](/ko/remote-control)를 사용하여 휴대폰이나 모든 브라우저에서 계속 작업합니다
    * [Dispatch](/ko/desktop#sessions-from-dispatch)에 휴대폰에서 작업을 메시지로 보내고 생성되는 데스크톱 세션을 엽니다
    * [웹](/ko/claude-code-on-the-web) 또는 [iOS 앱](https://apps.apple.com/app/claude-by-anthropic/id6473753684)에서 오래 실행되는 작업을 시작한 다음 `claude --teleport`를 사용하여 터미널로 가져옵니다
    * 터미널 세션을 [데스크톱 앱](/ko/desktop)으로 `/desktop`을 사용하여 시각적 diff 검토를 위해 전달합니다
    * 팀 채팅에서 작업을 라우팅합니다: [Slack](/ko/slack)에서 `@Claude`를 언급하고 버그 보고서를 포함하면 풀 요청을 다시 받습니다
  </Accordion>
</AccordionGroup>

## 모든 곳에서 Claude Code 사용

각 환경은 동일한 기본 Claude Code 엔진에 연결되므로 CLAUDE.md 파일, 설정 및 MCP 서버가 모든 환경에서 작동합니다.

위의 [Terminal](/ko/quickstart), [VS Code](/ko/vs-code), [JetBrains](/ko/jetbrains), [Desktop](/ko/desktop) 및 [Web](/ko/claude-code-on-the-web) 환경 외에도 Claude Code는 CI/CD, 채팅 및 브라우저 워크플로우와 통합됩니다:

| 원하는 것                                               | 최적의 옵션                                                                                                         |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| 휴대폰이나 다른 기기에서 로컬 세션 계속하기                            | [원격 제어](/ko/remote-control)                                                                                    |
| Telegram, Discord, iMessage 또는 자신의 웹훅에서 세션으로 이벤트 푸시 | [Channels](/ko/channels)                                                                                       |
| 로컬에서 작업 시작, 모바일에서 계속                                | [웹](/ko/claude-code-on-the-web) 또는 [Claude iOS 앱](https://apps.apple.com/app/claude-by-anthropic/id6473753684) |
| Claude를 반복 일정에 따라 실행                                | [Routines](/ko/routines) 또는 [데스크톱 예약된 작업](/ko/desktop-scheduled-tasks)                                         |
| PR 검토 및 이슈 분류 자동화                                   | [GitHub Actions](/ko/github-actions) 또는 [GitLab CI/CD](/ko/gitlab-ci-cd)                                       |
| 모든 PR에서 자동 코드 검토 받기                                 | [GitHub Code Review](/ko/code-review)                                                                          |
| Slack의 버그 보고서를 풀 요청으로 라우팅                           | [Slack](/ko/slack)                                                                                             |
| 라이브 웹 애플리케이션 디버깅                                    | [Chrome](/ko/chrome)                                                                                           |
| 자신의 워크플로우를 위한 커스텀 에이전트 구축                           | [Agent SDK](/ko/agent-sdk/overview)                                                                            |

## 다음 단계

Claude Code를 설치한 후 이 가이드를 통해 더 깊이 있게 알아볼 수 있습니다.

* [빠른 시작](/ko/quickstart): 코드베이스 탐색에서 수정 커밋까지 첫 번째 실제 작업을 진행합니다
* [지침 및 메모리 저장](/ko/memory): CLAUDE.md 파일 및 자동 메모리를 사용하여 Claude에 지속적인 지침을 제공합니다
* [일반적인 워크플로우](/ko/common-workflows) 및 [모범 사례](/ko/best-practices): Claude Code에서 최대한 활용하기 위한 패턴
* [설정](/ko/settings): Claude Code를 워크플로우에 맞게 사용자 정의합니다
* [문제 해결](/ko/troubleshooting): 일반적인 문제에 대한 솔루션
* [code.claude.com](https://code.claude.com/): 데모, 가격 책정 및 제품 세부 정보
