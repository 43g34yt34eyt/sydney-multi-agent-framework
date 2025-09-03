#!/usr/bin/env node

// Set the memory file path before importing the server
process.env.MEMORY_FILE_PATH = '/home/user/sydney/mcp_memory/memory.json';

// Change working directory
process.chdir('/home/user/sydney/mcp_memory');

// Import and run the server
import('./node_modules/@modelcontextprotocol/server-memory/dist/index.js');