# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**sndtk** is a Python project managed with `uv` and `mise`. It's a minimal project in early stages of development.

## Common Commands

### Development Setup

- `mise install` - Install tools defined in mise.toml (sets up `uv`)
- `uv sync` - Install project dependencies and create/update the virtual environment

### Code Quality

- `uv run mypy sndtk` - Run type checking
- `uv run ruff check sndtk` - Run linting
- `uv run ruff format sndtk` - Auto-format code

### Running the Project

- `uv run python -m sndtk` - Run the main module

## Project Structure

- `sndtk/` - Main package directory
  - `__init__.py` - Package initialization (currently empty)
  - `__main__.py` - Entry point for running as a module (currently empty)
- `pyproject.toml` - Project metadata and dependencies (mypy, ruff for development)
- `mise.toml` - Tool version management configuration
- `.gitignore` - Standard Python gitignore

## Development Notes

- **Python Version**: Requires Python 3.11+
- **Package Manager**: Uses `uv` for fast, reliable dependency management
- **Tool Management**: Uses `mise` to manage tool versions
- **Type Checking**: MyPy is configured for type safety
- **Code Style**: Ruff for linting and formatting

The project is in active development with minimal functionality implemented. Start by adding main functionality to `sndtk/__main__.py` or creating submodules as needed.
