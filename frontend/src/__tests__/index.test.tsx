import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Home from '../pages/index';

// Mock axios
jest.mock('axios');

describe('Home Page', () => {
  test('renders main heading', () => {
    render(<Home />);
    const heading = screen.getByText('文档分析系统');
    expect(heading).toBeInTheDocument();
  });

  test('renders file input', () => {
    render(<Home />);
    const fileInput = screen.getByRole('button', { name: /上传文件/i });
    expect(fileInput).toBeInTheDocument();
  });

  test('upload button is disabled when no file selected', () => {
    render(<Home />);
    const uploadButton = screen.getByRole('button', { name: /上传文件/i });
    expect(uploadButton).toBeDisabled();
  });
});