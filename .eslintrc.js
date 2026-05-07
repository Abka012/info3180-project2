module.exports = {
  rules: {
    'no-restricted-syntax': [
      {
        selector: 'CallExpression[callee.name="rgb"], CallExpression[callee.name="rgba"]',
        message: 'Use var(--token) instead of hardcoded rgb/rgba'
      },
      {
        selector: 'TemplateLiteral',
        message: 'No hardcoded colors in template literals'
      }
    ],
    'no-restricted-globals': [
      { name: /#[0-9a-f]{3,8}/, message: 'No hardcoded hex colors' }
    ],
    'no-restricted-imports': [
      { name: 'Pattern: #[0-9a-f]{3,8}', message: 'No hardcoded colors in imports' }
    ]
  }
}
