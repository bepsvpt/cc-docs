> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 快速入門

> 歡迎使用 Claude Code！

export const InstallConfigurator = () => {
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
      installLabel: 'Download the app',
      installHref: 'https://claude.com/download?utm_source=claude_code&utm_medium=docs&utm_content=configurator_desktop_download',
      guideHref: '/en/desktop-quickstart'
    },
    vscode: {
      name: 'VS Code',
      installLabel: 'Install from Marketplace',
      installHref: 'https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code',
      altCmd: 'code --install-extension anthropic.claude-code',
      guideHref: '/en/vs-code'
    },
    jetbrains: {
      name: 'JetBrains',
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
  const [target, setTarget] = useState('terminal');
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
.cc-ic-subtab-spacer { flex: 1; }
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
.cc-ic-cmd-toggle {
  display: flex; align-items: center; gap: 8px; font-family: inherit;
  background: none; border: none;
  padding: 0 12px; font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer; user-select: none; white-space: nowrap;
}
.cc-ic-cmd-toggle:hover { color: rgba(255, 255, 255, 0.75); }
.cc-ic-mini-check {
  width: 12px; height: 12px;
  border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 3px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.cc-ic-mini-check svg { color: #fff; display: none; }
.cc-ic-cmd-toggle.cc-ic-checked .cc-ic-mini-check { background: var(--ic-clay-deep); border-color: var(--ic-clay-deep); }
.cc-ic-cmd-toggle.cc-ic-checked .cc-ic-mini-check svg { display: block; }

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
  padding: 20px 22px;
  background: var(--ic-gray-000);
  border: 0.5px solid var(--ic-border-default);
  border-radius: 12px;
}
.cc-ic-handoff-head {
  font-size: 14px; line-height: 1.55; color: var(--ic-gray-700);
  margin-bottom: 14px;
}
.cc-ic-handoff-head strong { font-weight: 550; color: var(--ic-slate); }
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
            <span className="cc-ic-subtab-spacer" />
            {isWinInstaller && <button type="button" role="switch" aria-checked={winCmd} className={'cc-ic-cmd-toggle' + (winCmd ? ' cc-ic-checked' : '')} onClick={() => setWinCmd(!winCmd)}>
                <span className="cc-ic-mini-check">{iconCheck(9)}</span>
                <span>CMD instead of PowerShell</span>
              </button>}
          </div>
          {cardBodyCmd(terminalCmd, isWinPrompt ? '>' : '$')}
        </div>}

      {}
      {target === 'terminal' && <div className="cc-ic-below">
          {isWinInstaller && <span>
              Requires{' '}
              <a href="https://git-scm.com/downloads/win" target="_blank" rel="noopener">
                Git for Windows
              </a>.
            </span>}
          {(pkg === 'brew' || pkg === 'winget') && <span>
              Does not auto-update. Run{' '}
              <code>{pkg === 'brew' ? 'brew upgrade claude-code' : 'winget upgrade Anthropic.ClaudeCode'}</code>{' '}
              periodically.
            </span>}
          <a href="/en/troubleshooting">Troubleshooting</a>
        </div>}

      {alt && <div className="cc-ic-handoff">
          <div className="cc-ic-handoff-head">
            <strong>The steps below use the command line.</strong>{' '}
            Prefer {alt.name}? Install here, then follow the {alt.name} guide instead.
          </div>
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
    return {
      variant: bucket(flag, vid),
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

本快速入門指南將在幾分鐘內讓您使用 AI 驅動的編碼協助。完成後，您將了解如何使用 Claude Code 進行常見的開發任務。

<Experiment flag="quickstart-install-configurator" treatment={<InstallConfigurator />} />

## 開始前

確保您擁有：

* 已開啟的終端或命令提示字元
  * 如果您從未使用過終端，請查看[終端指南](/zh-TW/terminal-guide)
* 一個可以使用的程式碼專案
* 一個 [Claude 訂閱](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=quickstart_prereq)（Pro、Max、Teams 或 Enterprise）、[Claude Console](https://console.anthropic.com/) 帳戶，或透過[支援的雲端提供商](/zh-TW/third-party-integrations)存取

<Note>
  本指南涵蓋終端 CLI。Claude Code 也可在[網頁](https://claude.ai/code)、[桌面應用程式](/zh-TW/desktop)、[VS Code](/zh-TW/vs-code) 和 [JetBrains IDE](/zh-TW/jetbrains)、[Slack](/zh-TW/slack) 中使用，以及透過 [GitHub Actions](/zh-TW/github-actions) 和 [GitLab](/zh-TW/gitlab-ci-cd) 進行 CI/CD。請參閱[所有介面](/zh-TW/overview#use-claude-code-everywhere)。
</Note>

## 步驟 1：安裝 Claude Code

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. Use the PowerShell command above instead. Your prompt shows `PS C:\` when you're in PowerShell.

    **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell  theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

## 步驟 2：登入您的帳戶

Claude Code 需要帳戶才能使用。當您使用 `claude` 命令啟動互動式工作階段時，您需要登入：

```bash  theme={null}
claude
# 首次使用時系統會提示您登入
```

```bash  theme={null}
/login
# 按照提示使用您的帳戶登入
```

您可以使用以下任何帳戶類型登入：

* [Claude Pro、Max、Teams 或 Enterprise](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=quickstart_login)（推薦）
* [Claude Console](https://console.anthropic.com/)（具有預付額度的 API 存取）。首次登入時，Console 中會自動建立「Claude Code」工作區以進行集中成本追蹤。
* [Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry](/zh-TW/third-party-integrations)（企業雲端提供商）

登入後，您的認證將被儲存，您無需再次登入。若要稍後切換帳戶，請使用 `/login` 命令。

## 步驟 3：啟動您的第一個工作階段

在任何專案目錄中開啟您的終端並啟動 Claude Code：

```bash  theme={null}
cd /path/to/your/project
claude
```

您將看到 Claude Code 歡迎畫面，其中包含您的工作階段資訊、最近的對話和最新更新。輸入 `/help` 以查看可用命令，或輸入 `/resume` 以繼續之前的對話。

<Tip>
  登入後（步驟 2），您的認證將儲存在您的系統上。在[認證管理](/zh-TW/authentication#credential-management)中了解更多。
</Tip>

## 步驟 4：提出您的第一個問題

讓我們從了解您的程式碼庫開始。嘗試以下命令之一：

```text  theme={null}
what does this project do?
```

Claude 將分析您的檔案並提供摘要。您也可以提出更具體的問題：

```text  theme={null}
what technologies does this project use?
```

```text  theme={null}
where is the main entry point?
```

```text  theme={null}
explain the folder structure
```

您也可以詢問 Claude 其自身的功能：

```text  theme={null}
what can Claude Code do?
```

```text  theme={null}
how do I create custom skills in Claude Code?
```

```text  theme={null}
can Claude Code work with Docker?
```

<Note>
  Claude Code 會根據需要讀取您的專案檔案。您無需手動新增內容。
</Note>

## 步驟 5：進行您的第一次程式碼變更

現在讓我們讓 Claude Code 進行一些實際的編碼。嘗試一個簡單的任務：

```text  theme={null}
add a hello world function to the main file
```

Claude Code 將：

1. 找到適當的檔案
2. 向您顯示建議的變更
3. 要求您的批准
4. 進行編輯

<Note>
  Claude Code 在修改檔案前始終要求許可。您可以批准個別變更或為工作階段啟用「全部接受」模式。
</Note>

## 步驟 6：使用 Git 與 Claude Code

Claude Code 使 Git 操作變得對話式：

```text  theme={null}
what files have I changed?
```

```text  theme={null}
commit my changes with a descriptive message
```

您也可以提示進行更複雜的 Git 操作：

```text  theme={null}
create a new branch called feature/quickstart
```

```text  theme={null}
show me the last 5 commits
```

```text  theme={null}
help me resolve merge conflicts
```

## 步驟 7：修復錯誤或新增功能

Claude 擅長除錯和功能實現。

用自然語言描述您想要的內容：

```text  theme={null}
add input validation to the user registration form
```

或修復現有問題：

```text  theme={null}
there's a bug where users can submit empty forms - fix it
```

Claude Code 將：

* 定位相關程式碼
* 理解上下文
* 實現解決方案
* 如果可用，執行測試

## 步驟 8：測試其他常見工作流程

有許多方式可以與 Claude 合作：

**重構程式碼**

```text  theme={null}
refactor the authentication module to use async/await instead of callbacks
```

**編寫測試**

```text  theme={null}
write unit tests for the calculator functions
```

**更新文件**

```text  theme={null}
update the README with installation instructions
```

**程式碼審查**

```text  theme={null}
review my changes and suggest improvements
```

<Tip>
  像與有幫助的同事交談一樣與 Claude 交談。描述您想要達成的目標，它將幫助您實現。
</Tip>

## 基本命令

以下是日常使用中最重要的命令：

| 命令                  | 功能             | 範例                                  |
| ------------------- | -------------- | ----------------------------------- |
| `claude`            | 啟動互動模式         | `claude`                            |
| `claude "task"`     | 執行一次性任務        | `claude "fix the build error"`      |
| `claude -p "query"` | 執行一次性查詢，然後退出   | `claude -p "explain this function"` |
| `claude -c`         | 在目前目錄中繼續最近的對話  | `claude -c`                         |
| `claude -r`         | 恢復之前的對話        | `claude -r`                         |
| `claude commit`     | 建立 Git 提交      | `claude commit`                     |
| `/clear`            | 清除對話歷史         | `/clear`                            |
| `/help`             | 顯示可用命令         | `/help`                             |
| `exit` 或 Ctrl+C     | 退出 Claude Code | `exit`                              |

請參閱 [CLI 參考](/zh-TW/cli-reference)以取得完整的命令清單。

## 初學者的專業提示

如需更多資訊，請參閱[最佳實踐](/zh-TW/best-practices)和[常見工作流程](/zh-TW/common-workflows)。

<AccordionGroup>
  <Accordion title="對您的請求要具體">
    不要這樣做：'修復錯誤'

    試試這樣：'修復登入錯誤，使用者輸入錯誤認證後看到空白畫面'
  </Accordion>

  <Accordion title="使用逐步說明">
    將複雜任務分解為步驟：

    ```text  theme={null}
    1. create a new database table for user profiles
    2. create an API endpoint to get and update user profiles
    3. build a webpage that allows users to see and edit their information
    ```
  </Accordion>

  <Accordion title="讓 Claude 先探索">
    在進行變更之前，讓 Claude 了解您的程式碼：

    ```text  theme={null}
    analyze the database schema
    ```

    ```text  theme={null}
    build a dashboard showing products that are most frequently returned by our UK customers
    ```
  </Accordion>

  <Accordion title="使用快捷方式節省時間">
    * 按 `?` 查看所有可用的快捷鍵
    * 使用 Tab 進行命令完成
    * 按 ↑ 查看命令歷史
    * 輸入 `/` 查看所有命令和 skills
  </Accordion>
</AccordionGroup>

## 接下來呢？

現在您已經學習了基礎知識，請探索更多進階功能：

<CardGroup cols={2}>
  <Card title="Claude Code 如何運作" icon="microchip" href="/zh-TW/how-claude-code-works">
    了解代理迴圈、內建工具以及 Claude Code 如何與您的專案互動
  </Card>

  <Card title="最佳實踐" icon="star" href="/zh-TW/best-practices">
    透過有效的提示和專案設定獲得更好的結果
  </Card>

  <Card title="常見工作流程" icon="graduation-cap" href="/zh-TW/common-workflows">
    常見任務的逐步指南
  </Card>

  <Card title="擴展 Claude Code" icon="puzzle-piece" href="/zh-TW/features-overview">
    使用 CLAUDE.md、skills、hooks、MCP 等進行自訂
  </Card>
</CardGroup>

## 獲取幫助

* **在 Claude Code 中**：輸入 `/help` 或詢問「how do I...」
* **文件**：您在這裡！瀏覽其他指南
* **社群**：加入我們的 [Discord](https://www.anthropic.com/discord) 以獲取提示和支援
