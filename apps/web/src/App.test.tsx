import { render, screen } from '@testing-library/react';
import { expect, test } from 'vitest';
import { App } from './App';

test('identifies the project and communicates its scientific limitations', () => {
  render(<App />);
  expect(screen.getByRole('heading', { name: 'Lunar Navigator' })).toBeInTheDocument();
  expect(screen.getByText(/Scientific features are not yet implemented/)).toBeInTheDocument();
  expect(screen.getByText(/Not a landing-safety certification system/)).toBeInTheDocument();
});
