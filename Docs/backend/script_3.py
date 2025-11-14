
# Create .babelrc
babelrc = '''{
  "presets": [
    "@babel/preset-env",
    ["@babel/preset-react", { "runtime": "automatic" }]
  ]
}
'''

with open('greenfuel-frontend/.babelrc', 'w') as f:
    f.write(babelrc)

# Create .env.example
env_example = '''# Backend API Configuration
REACT_APP_API_BASE_URL=http://localhost:5000
REACT_APP_API_TIMEOUT=30000

# Feature Flags
REACT_APP_USE_MOCK_PREDICTIONS=false
REACT_APP_DEBUG_MODE=false

# Analytics (Optional)
REACT_APP_GA_ID=
'''

with open('greenfuel-frontend/.env.example', 'w') as f:
    f.write(env_example)

print("✓ Created .babelrc and .env.example")
