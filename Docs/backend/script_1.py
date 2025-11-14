
# Create package.json
package_json = '''{
  "name": "greenfuel-ml-frontend",
  "version": "1.0.0",
  "description": "Professional React-based frontend for GreenFuel-ML hydrogen production prediction",
  "main": "index.js",
  "scripts": {
    "start": "webpack serve --mode development",
    "build": "webpack --mode production",
    "dev": "webpack --mode development --watch",
    "serve": "python -m http.server 8000 --directory dist"
  },
  "keywords": ["hydrogen", "prediction", "machine-learning", "react"],
  "author": "Yuvraj Barot",
  "license": "MIT",
  "devDependencies": {
    "@babel/core": "^7.23.0",
    "@babel/preset-env": "^7.23.0",
    "@babel/preset-react": "^7.22.0",
    "babel-loader": "^9.1.0",
    "css-loader": "^6.8.0",
    "style-loader": "^3.3.0",
    "webpack": "^5.89.0",
    "webpack-cli": "^5.1.0",
    "webpack-dev-server": "^4.15.0",
    "html-webpack-plugin": "^5.5.3"
  },
  "dependencies": {
    "axios": "^1.6.0",
    "chart.js": "^4.4.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.16.0"
  }
}
'''

with open('greenfuel-frontend/package.json', 'w') as f:
    f.write(package_json)

print("✓ Created package.json")
