<h1>🧠 Connect 4 AI Agent (Minimax + Alpha-Beta Pruning)</h1>

<p>This is a Python-based Connect 4 game featuring a powerful AI opponent built using the <strong>Minimax algorithm with Alpha-Beta pruning</strong>. The game includes a graphical interface built with Pygame and supports human vs. AI gameplay.</p>

<hr>

<h2>📦 Requirements</h2>

<p>Make sure you have <strong>Python 3.7+</strong> installed.</p>

<h3>Required Python Packages:</h3>
<pre><code>pip install pygame numpy
</code></pre>

<hr>

<h2>▶️ How to Run the Game</h2>

<ol>
  <li><strong>Clone this repository</strong> or download the project files:</li>
</ol>

<pre><code>git clone https://github.com/your-username/connect4-ai.git
cd connect4-ai
</code></pre>

<ol start="2">
  <li><strong>Run the main Python script:</strong></li>
</ol>

<pre><code>python connect4.py
</code></pre>

<hr>

<h2>🕹️ Gameplay Instructions</h2>

<ul>
  <li>The game launches in a <strong>graphical window</strong>.</li>
  <li>You (the human player) always play first and are represented by <strong>red discs</strong>.</li>
  <li>The AI plays second and is represented by <strong>yellow discs</strong>.</li>
  <li>To place a move, <strong>click on the desired column</strong> in the window.</li>
  <li>The first player to connect 4 of their discs horizontally, vertically, or diagonally wins.</li>
</ul>

<hr>

<h2>🧠 AI Strategy</h2>

<ul>
  <li>Uses the <strong>Minimax algorithm</strong> with <strong>Alpha-Beta pruning</strong>.</li>
  <li>Evaluates board positions with a heuristic scoring function.</li>
  <li>Plays up to a configurable <strong>depth (default is 6)</strong> for a strong but responsive opponent.</li>
  <li>Makes blocking and winning moves intelligently.</li>
</ul>

<hr>

