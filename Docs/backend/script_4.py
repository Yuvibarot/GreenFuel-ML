
# Create public/index.html - Entry point (minimal)
public_index = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GreenFuel-ML: Hydrogen Production Predictor</title>
    <link rel="stylesheet" href="../src/style.css">
</head>
<body>
    <div id="root"></div>
    <script src="../src/app.js"></script>
</body>
</html>
'''

with open('greenfuel-frontend/public/index.html', 'w') as f:
    f.write(public_index)

print("✓ Created public/index.html")
