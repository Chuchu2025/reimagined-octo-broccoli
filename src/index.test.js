const test = require('node:test');
const assert = require('node:assert');
const { greet } = require('./index.js');

test('greet function returns correct message with name', () => {
  const result = greet('Alice');
  assert.strictEqual(result, 'Hello, Alice!');
});

test('greet function returns default message without name', () => {
  const result = greet();
  assert.strictEqual(result, 'Hello, World!');
});

test('greet function handles empty string', () => {
  const result = greet('');
  assert.strictEqual(result, 'Hello, !');
});
