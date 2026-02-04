<h1 align="center">eSim Tools Manager</h1>

<p align="center">
  A command-line tool to install, inspect, and validate tools used in
  <strong>eSim-based circuit and HDL workflows</strong>.
</p>

<p>
  The project focuses on <strong>automation where it is safe</strong>, and
  <strong>explicit user control</strong> where system-level changes are risky.
</p>

<p>
  This is a <strong>modular, extensible tool manager</strong>, implemented in Python,
  with real installation logic for selected tools and
  dependency-aware checks for others.
</p>

<hr>

<h2>✨ What This Tool Does</h2>
<ul>
  <li>Provides a single CLI to manage eSim-related tools</li>
  <li>Installs selected tools with OS-specific logic</li>
  <li>Detects installed tools using system PATH</li>
  <li>Extracts and compares tool versions</li>
  <li>Validates system readiness using a <code>doctor</code> command</li>
  <li>Handles NGHDL dependencies intelligently</li>
</ul>

<hr>

<h2>🧠 Managed vs Dependency-Based Tools</h2>

<h3>🔧 Managed Tools (direct install / update support)</h3>
<p>These tools have explicit installer logic implemented in the code:</p>
<ul>
  <li><strong>ngspice</strong></li>
  <li><strong>KiCad</strong></li>
  <li><strong>NGHDL</strong> (handled via eSim detection + dependency checks)</li>
</ul>

<h3>🔗 NGHDL Dependency Tools</h3>
<p>The following tools are not managed independently, but are checked only during NGHDL installation:</p>
<ul>
  <li>ghdl</li>
  <li>verilator</li>
  <li>ngspice</li>
</ul>

<h4>How this works</h4>
<ul>
  <li>NGHDL is bundled with eSim</li>
  <li>If eSim exists, NGHDL is assumed to exist</li>
  <li>Required dependencies are detected via system PATH</li>
  <li>Missing dependencies are reported</li>
  <li>Installation happens only after user confirmation</li>
  <li>Installation behavior depends on the operating system</li>
</ul>

<p>
  This design avoids unsafe global installations and respects platform limitations.
</p>

<hr>

<h2>🏗 Architecture Overview</h2>

<pre>
User
 ↓
CLI (argparse)
 ↓
Command Router (cli.py)
 ↓
--------------------------------
| Installer | Dependency Check |
| Version Engine | Doctor Mode |
--------------------------------
 ↓
OS-specific execution
(Linux / Windows / macOS)
</pre>

<hr>

<h2>🧩 Core Components</h2>

<h3>CLI (<code>cli.py</code>)</h3>
<ul>
  <li>Entry point for the tool</li>
  <li>Handles commands:
    <ul>
      <li>install</li>
      <li>update</li>
      <li>list</li>
      <li>doctor</li>
      <li>version</li>
      <li>help</li>
    </ul>
  </li>
</ul>

<h3>Tool Configuration (<code>tools.yml</code>)</h3>
<ul>
  <li>Tool detection logic</li>
  <li>Version commands</li>
  <li>Minimum / recommended versions</li>
  <li>Install metadata</li>
  <li>Dependency definitions</li>
</ul>

<h3>Dependency Engine (<code>dependency.py</code>)</h3>
<ul>
  <li>Detects executables and directories</li>
  <li>Extracts installed versions</li>
  <li>Compares versions using semantic versioning</li>
  <li>Implements the <code>doctor</code> command</li>
  <li>Decides whether an update is required</li>
</ul>

<h3>Installer (<code>installer.py</code>)</h3>
<ul>
  <li>Controls which tools can be installed or updated automatically</li>
  <li>Prevents updates for unmanaged tools</li>
  <li>Routes installation to tool-specific logic</li>
</ul>

<h3>Version Handling (<code>version.py</code>)</h3>
<ul>
  <li>Extracts versions from command output</li>
  <li>Uses <code>packaging.version</code> for reliable comparison</li>
  <li>Distinguishes between:
    <ul>
      <li>outdated</li>
      <li>acceptable</li>
      <li>recommended update</li>
    </ul>
  </li>
</ul>

<h3>Tool-Specific Installers</h3>
<ul>
  <li><code>ngspice.py</code></li>
  <li><code>kicad.py</code></li>
  <li><code>nghdl.py</code></li>
</ul>

<p>
  These files contain OS-aware, real install logic — not placeholders.
</p>

<hr>

<h2>🚀 Installation</h2>

<h3>Prerequisites</h3>
<ul>
  <li>Python 3.8 or higher</li>
  <li>pip</li>
</ul>

<h3>Install the Tool Manager</h3>

<pre>
git clone &lt;repository-url&gt;
cd esim-tools-manager
pip install .
</pre>

<p>After installation, the CLI becomes available as:</p>
<pre>esim-tools</pre>

<hr>

<h2>🖥 CLI Usage</h2>

<h3>Show help</h3>
<pre>esim-tools help</pre>

<h3>Show tool manager version</h3>
<pre>esim-tools version</pre>

<h3>List detected tools</h3>
<pre>esim-tools list</pre>

<h3>Install tools</h3>
<pre>
esim-tools install ngspice
esim-tools install kicad
esim-tools install nghdl
esim-tools install all
</pre>

<h3>Update tools</h3>
<pre>
esim-tools update ngspice
esim-tools update all
</pre>

<h3>Run system diagnostics</h3>
<pre>esim-tools doctor</pre>

<hr>

<h2>🧭 Platform-Specific Behavior</h2>

<h3>Linux</h3>
<ul>
  <li>Uses apt where applicable</li>
  <li>Builds ngspice from source when required</li>
  <li>Can auto-install NGHDL dependencies</li>
</ul>

<h3>Windows</h3>
<ul>
  <li>Uses compressed archives or installers</li>
  <li>Some tools require manual installation</li>
  <li>Clear instructions are shown instead of unsafe automation</li>
</ul>

<h3>macOS</h3>
<ul>
  <li>Uses Homebrew when available</li>
  <li>Falls back safely if brew is missing</li>
</ul>

<hr>

<h2>🎯 Design Philosophy</h2>
<ul>
  <li><strong>Automation with boundaries</strong></li>
  <li><strong>YAML-driven configuration</strong></li>
  <li><strong>Dependency-aware installs</strong></li>
  <li><strong>CLI-first approach</strong></li>
  <li><strong>Extensible by design</strong></li>
</ul>

<hr>

<h2>⚠ Known Limitations</h2>
<ul>
  <li>No dependency graph resolution</li>
  <li>No rollback for failed installs</li>
  <li>Windows support is partially manual</li>
  <li>No background update checks</li>
</ul>

<p>These are intentional tradeoffs, not bugs.</p>

<hr>

<h2>🔮 Future Improvements</h2>
<ul>
  <li>Non-interactive install mode</li>
  <li>Configurable install directories</li>
  <li>Plugin-based tool definitions</li>
  <li>Logging and dry-run support</li>
  <li>Smarter dependency resolution</li>
</ul>

<hr>

<h2>📄 License</h2>
<p>MIT License</p>
