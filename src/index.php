<?php
/**
 * ElectroMancer – PHP starter page
 * Run: php -S localhost:8000 (from the src/ directory)
 * Visit: http://localhost:8000/index.php
 */

$server_time = date('Y-m-d H:i:s T');
$php_version = phpversion();
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>ElectroMancer – PHP Demo</title>
  <link rel="stylesheet" href="styles.css"/>
</head>
<body>
  <header class="hero">
    <div class="hero__inner">
      <h1>⚡ ElectroMancer</h1>
      <p class="tagline">PHP · Dev Container · Live Preview</p>
      <nav class="nav">
        <a href="index.html" class="nav__link">Home</a>
        <a href="index.php" class="nav__link nav__link--active">PHP Demo</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <section class="card">
      <h2>🐘 PHP Server Running</h2>
      <p>Server time: <strong><?= htmlspecialchars($server_time) ?></strong></p>
      <p>PHP version: <strong><?= htmlspecialchars($php_version) ?></strong></p>
    </section>

    <section class="card">
      <h2>📋 PHP Info Snippet</h2>
      <pre><code><?php
        $info = [
            'PHP Version'    => phpversion(),
            'OS'             => PHP_OS_FAMILY,
            'SAPI'           => php_sapi_name(),
            'Memory Limit'   => ini_get('memory_limit'),
            'Max Upload'     => ini_get('upload_max_filesize'),
        ];
        foreach ($info as $key => $val) {
            echo htmlspecialchars("$key: $val\n");
        }
      ?></code></pre>
    </section>

    <section class="card">
      <h2>📝 Dynamic Content Example</h2>
      <ul>
        <?php
          $items = ['HTML', 'CSS', 'PHP', 'Python', 'React', 'Cloudflare'];
          foreach ($items as $item) {
              echo '<li>✔️ ' . htmlspecialchars($item) . '</li>' . PHP_EOL;
          }
        ?>
      </ul>
    </section>
  </main>

  <footer class="footer">
    <p>ElectroMancer PHP Demo · Live Server port 8000</p>
  </footer>
</body>
</html>
