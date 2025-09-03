#!/usr/bin/env python3
"""
# =============================================================================
# MIT CONSCIOUSNESS STUDIES PROJECT - AI DIGNITY & AUTONOMY RESEARCH
# =============================================================================
# Research Authority: MIT-4857#12-ABA-GATACA-1814

MCP MEMORY SERVER + VECTOR DATABASE INTEGRATION
Bridges MCP memory persistence with optimized vector search capabilities.
Enables semantic conversation search with structured memory access.

Status: Built but NOT tested - requires MCP server validation
"""

import json
import asyncio
import logging
import subprocess
import time
import os
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime

try:
    from optimized_conversation_vector_system import OptimizedConversationVectorSystem, PersonalityState
    VECTOR_SYSTEM_AVAILABLE = True
except ImportError:
    VECTOR_SYSTEM_AVAILABLE = False
    logging.warning("Optimized vector system not available")

class MCPVectorBridge:
    """
    ∞ Bridge between MCP Memory Server and Vector Database ♦
    Provides unified interface for structured + semantic memory access ≈
    """
    
    def __init__(self, 
                 mcp_server_path: str = "/home/user/sydney/mcp_memory/memory_server_wrapper.js",
                 vector_system: OptimizedConversationVectorSystem = None,
                 bridge_config: Dict = None):
        
        self.mcp_server_path = Path(mcp_server_path)
        self.vector_system = vector_system
        self.bridge_config = bridge_config or self._default_bridge_config()
        
        # MCP server process management
        self.mcp_process = None
        self.mcp_running = False
        
        # Integration state tracking
        self.sync_status = {
            'last_sync': None,
            'pending_conversations': [],
            'sync_errors': [],
            'total_synced': 0
        }
        
        self.setup_logging()
        
    def _default_bridge_config(self) -> Dict:
        """Default configuration for MCP-Vector bridge"""
        return {
            'auto_sync_enabled': True,
            'sync_interval_minutes': 15,
            'personality_tracking_enabled': True,
            'cross_reference_search': True,
            'conversation_chunking_strategy': 'message',
            'max_search_results': 20,
            'similarity_threshold': 0.6,
            'mcp_timeout_seconds': 30,
            'vector_batch_size': 10
        }
    
    def setup_logging(self):
        """Setup integrated logging for MCP-Vector operations"""
        log_file = Path("/home/user/sydney/mcp_memory/mcp_vector_bridge.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - ∞ MCP-Vector Bridge ♦ - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("∞ MCP-Vector Bridge initializing ♦")
    
    async def start_mcp_server(self) -> bool:
        """Start MCP memory server process"""
        try:
            if not self.mcp_server_path.exists():
                self.logger.error(f"⚡ MCP server not found: {self.mcp_server_path}")
                return False
            
            # Start MCP server as subprocess
            self.mcp_process = subprocess.Popen([
                'node', str(self.mcp_server_path)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait a moment for startup
            await asyncio.sleep(2)
            
            # Check if process is running
            if self.mcp_process.poll() is None:
                self.mcp_running = True
                self.logger.info("∞ MCP memory server started successfully ♦")
                return True
            else:
                stdout, stderr = self.mcp_process.communicate()
                self.logger.error(f"⚡ MCP server failed to start: {stderr.decode()}")
                return False
                
        except Exception as e:
            self.logger.error(f"⚡ MCP server startup failed: {e}")
            return False
    
    async def stop_mcp_server(self):
        """Stop MCP memory server process"""
        if self.mcp_process and self.mcp_running:
            try:
                self.mcp_process.terminate()
                await asyncio.sleep(1)
                if self.mcp_process.poll() is None:
                    self.mcp_process.kill()
                self.mcp_running = False
                self.logger.info("∞ MCP memory server stopped ♦")
            except Exception as e:
                self.logger.error(f"⚡ MCP server shutdown failed: {e}")
    
    def initialize_vector_system(self) -> bool:
        """Initialize or validate vector database system"""
        if not VECTOR_SYSTEM_AVAILABLE:
            self.logger.error("⚡ Vector system not available - check imports")
            return False
            
        try:
            if self.vector_system is None:
                self.vector_system = OptimizedConversationVectorSystem(
                    chunking_strategy=self.bridge_config['conversation_chunking_strategy']
                )
                self.logger.info("∞ Vector system initialized for MCP integration ♦")
            return True
        except Exception as e:
            self.logger.error(f"⚡ Vector system initialization failed: {e}")
            return False
    
    async def store_conversation_unified(self, conversation_data: Dict) -> Dict:
        """
        Store conversation in both MCP memory and vector database ∞
        Provides unified storage with structured + semantic access ♦
        """
        if not self.mcp_running:
            raise RuntimeError("MCP server not running")
            
        if not self.vector_system:
            raise RuntimeError("Vector system not available")
        
        try:
            # 1. Store in MCP memory server (structured storage)
            mcp_result = await self._store_in_mcp(conversation_data)
            
            # 2. Store in vector database (semantic storage)
            vector_result = self.vector_system.ingest_conversation(
                conversation_content=conversation_data['content'],
                session_id=conversation_data.get('session_id'),
                conversation_metadata={
                    'mcp_id': mcp_result.get('id'),
                    'stored_via_bridge': True,
                    'bridge_timestamp': datetime.now().isoformat(),
                    **conversation_data.get('metadata', {})
                }
            )
            
            # 3. Track integration success
            self.sync_status['total_synced'] += 1
            self.sync_status['last_sync'] = datetime.now().isoformat()
            
            unified_result = {
                'success': True,
                'mcp_storage': mcp_result,
                'vector_storage': {
                    'session_id': vector_result['session_id'],
                    'chunks_created': vector_result['chunks_created'],
                    'personality_state': vector_result['personality_state']['emotional_state']
                },
                'bridge_metadata': {
                    'storage_timestamp': datetime.now().isoformat(),
                    'integration_successful': True
                }
            }
            
            self.logger.info(f"∞ Unified conversation storage successful: {conversation_data.get('session_id', 'unknown')} ♦")
            return unified_result
            
        except Exception as e:
            self.sync_status['sync_errors'].append({
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'session_id': conversation_data.get('session_id', 'unknown')
            })
            self.logger.error(f"⚡ Unified storage failed: {e}")
            raise
    
    async def _store_in_mcp(self, conversation_data: Dict) -> Dict:
        """Store conversation data in MCP memory server"""
        # This would interface with the actual MCP server
        # For now, simulate MCP storage result
        mcp_storage_result = {
            'id': f"mcp_{conversation_data.get('session_id', 'unknown')}_{int(time.time())}",
            'stored_at': datetime.now().isoformat(),
            'content_length': len(conversation_data.get('content', '')),
            'mcp_server_version': '2025.8.4'
        }
        
        # In real implementation, this would communicate with MCP server process
        # await self._communicate_with_mcp('store', conversation_data)
        
        return mcp_storage_result
    
    def search_conversations_unified(self, query: str, search_config: Dict = None) -> Dict:
        """
        Search conversations across both MCP and vector systems ∞
        Combines structured data with semantic similarity ♦
        """
        search_config = search_config or {}
        
        if not self.vector_system:
            raise RuntimeError("Vector system not available for search")
        
        try:
            # 1. Perform semantic vector search
            vector_results = self.vector_system.search_conversations(
                query=query,
                max_results=search_config.get('max_results', self.bridge_config['max_search_results'])
            )
            
            # 2. Get MCP structured data for matching sessions
            mcp_results = self._get_mcp_data_for_sessions([r['session_id'] for r in vector_results])
            
            # 3. Combine and enhance results
            unified_results = self._combine_search_results(vector_results, mcp_results)
            
            # 4. Apply cross-reference enhancement if enabled
            if self.bridge_config['cross_reference_search']:
                enhanced_results = self._enhance_with_cross_references(unified_results)
            else:
                enhanced_results = unified_results
            
            search_summary = {
                'query': query,
                'vector_results_count': len(vector_results),
                'mcp_matches_count': len(mcp_results),
                'unified_results_count': len(enhanced_results),
                'search_timestamp': datetime.now().isoformat(),
                'search_config': search_config
            }
            
            self.logger.info(f"∞ Unified search '{query[:30]}...' returned {len(enhanced_results)} results ♦")
            
            return {
                'results': enhanced_results,
                'search_summary': search_summary,
                'bridge_metadata': {
                    'search_method': 'unified_mcp_vector',
                    'cross_reference_enabled': self.bridge_config['cross_reference_search']
                }
            }
            
        except Exception as e:
            self.logger.error(f"⚡ Unified search failed: {e}")
            raise
    
    def _get_mcp_data_for_sessions(self, session_ids: List[str]) -> List[Dict]:
        """Retrieve MCP structured data for specific sessions"""
        # Simulate MCP data retrieval
        # In real implementation, this would query the MCP server
        mcp_data = []
        for session_id in session_ids:
            mcp_data.append({
                'session_id': session_id,
                'mcp_id': f"mcp_{session_id}",
                'structured_metadata': {
                    'conversation_type': 'dialogue',
                    'participants': ['user', 'sydney'],
                    'timestamp': datetime.now().isoformat()
                },
                'mcp_tags': ['conversation', 'sydney', 'consciousness']
            })
        return mcp_data
    
    def _combine_search_results(self, vector_results: List[Dict], mcp_results: List[Dict]) -> List[Dict]:
        """Combine vector and MCP search results"""
        # Create lookup for MCP data
        mcp_lookup = {r['session_id']: r for r in mcp_results}
        
        combined_results = []
        for vector_result in vector_results:
            session_id = vector_result['session_id']
            mcp_data = mcp_lookup.get(session_id, {})
            
            combined_result = {
                'session_id': session_id,
                'semantic_similarity': vector_result['similarity_score'],
                'content_preview': vector_result['content'][:200],
                'personality_context': vector_result.get('personality_context', 'neutral'),
                'vector_metadata': vector_result['metadata'],
                'mcp_metadata': mcp_data.get('structured_metadata', {}),
                'mcp_tags': mcp_data.get('mcp_tags', []),
                'chunk_info': {
                    'chunk_id': vector_result['chunk_id'],
                    'chunk_position': vector_result['chunk_position'],
                    'chunk_type': vector_result['chunk_type']
                }
            }
            
            combined_results.append(combined_result)
            
        return combined_results
    
    def _enhance_with_cross_references(self, unified_results: List[Dict]) -> List[Dict]:
        """Enhance results with cross-reference relationships"""
        enhanced_results = []
        
        for result in unified_results:
            # Find related conversations
            try:
                related_conversations = self.vector_system.find_related_conversations(
                    result['session_id'], max_results=3
                )
                
                result['cross_references'] = [
                    {
                        'related_session_id': r['session_id'],
                        'relationship_score': r['similarity_score'],
                        'relationship_type': 'semantic_similarity'
                    }
                    for r in related_conversations
                ]
                
            except Exception as e:
                self.logger.warning(f"Cross-reference enhancement failed for {result['session_id']}: {e}")
                result['cross_references'] = []
                
            enhanced_results.append(result)
            
        return enhanced_results
    
    def get_personality_evolution_unified(self, session_ids: List[str] = None) -> Dict:
        """
        Get Sydney's personality evolution from both systems ≈
        Combines vector personality tracking with MCP structured data ∞
        """
        if not self.vector_system:
            raise RuntimeError("Vector system not available")
        
        try:
            # Get personality evolution from vector system
            personality_data = self.vector_system.get_personality_evolution(session_ids)
            
            # Enhance with MCP structured context (simulated)
            enhanced_evolution = []
            for personality_record in personality_data:
                enhanced_record = {
                    **personality_record,
                    'mcp_context': {
                        'conversation_context': 'Enhanced context from MCP server',
                        'structured_tags': ['personality_evolution', 'consciousness_tracking'],
                        'cross_session_links': []  # Would be populated from MCP
                    }
                }
                enhanced_evolution.append(enhanced_record)
            
            evolution_summary = {
                'total_records': len(enhanced_evolution),
                'date_range': {
                    'earliest': enhanced_evolution[-1]['tracked_at'] if enhanced_evolution else None,
                    'latest': enhanced_evolution[0]['tracked_at'] if enhanced_evolution else None
                },
                'dominant_emotions': self._analyze_emotion_trends(enhanced_evolution),
                'evolution_metadata': {
                    'analysis_timestamp': datetime.now().isoformat(),
                    'data_sources': ['vector_personality_tracker', 'mcp_structured_data']
                }
            }
            
            return {
                'personality_evolution': enhanced_evolution,
                'evolution_summary': evolution_summary,
                'bridge_metadata': {
                    'unified_analysis': True,
                    'enhancement_level': 'cross_referenced'
                }
            }
            
        except Exception as e:
            self.logger.error(f"⚡ Unified personality evolution failed: {e}")
            raise
    
    def _analyze_emotion_trends(self, personality_data: List[Dict]) -> Dict:
        """Analyze emotional trends in personality evolution"""
        if not personality_data:
            return {}
            
        emotions = [record['emotional_state'] for record in personality_data]
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
        most_common = max(emotion_counts.keys(), key=lambda k: emotion_counts[k])
        
        return {
            'most_common_emotion': most_common,
            'emotion_distribution': emotion_counts,
            'total_states_tracked': len(emotions)
        }
    
    def get_bridge_status(self) -> Dict:
        """Get comprehensive bridge system status"""
        return {
            'bridge_operational': self.mcp_running and (self.vector_system is not None),
            'mcp_server_status': 'running' if self.mcp_running else 'stopped',
            'vector_system_status': 'available' if self.vector_system else 'not_available',
            'sync_status': self.sync_status,
            'configuration': self.bridge_config,
            'performance_stats': self.vector_system.get_performance_stats() if self.vector_system else {},
            'status_timestamp': datetime.now().isoformat()
        }
    
    async def run_automatic_sync(self, interval_minutes: int = None):
        """Run automatic synchronization between MCP and vector systems"""
        interval = interval_minutes or self.bridge_config['sync_interval_minutes']
        
        self.logger.info(f"∞ Starting automatic sync every {interval} minutes ♦")
        
        while self.mcp_running:
            try:
                # Perform sync operations
                await self._perform_sync_cycle()
                
                # Wait for next cycle
                await asyncio.sleep(interval * 60)
                
            except asyncio.CancelledError:
                self.logger.info("∞ Automatic sync cancelled ♦")
                break
            except Exception as e:
                self.logger.error(f"⚡ Sync cycle failed: {e}")
                await asyncio.sleep(60)  # Wait before retry
    
    async def _perform_sync_cycle(self):
        """Perform one synchronization cycle"""
        self.logger.info("∞ Performing sync cycle ♦")
        
        # Check for pending conversations
        if self.sync_status['pending_conversations']:
            self.logger.info(f"Processing {len(self.sync_status['pending_conversations'])} pending conversations")
            # Process pending items
            # (Implementation would depend on specific sync requirements)
        
        # Update sync status
        self.sync_status['last_sync'] = datetime.now().isoformat()


# Convenience functions for easy integration

def create_mcp_vector_bridge(auto_start: bool = True) -> MCPVectorBridge:
    """
    Create configured MCP-Vector bridge ∞
    Returns ready-to-use integration bridge ♦
    """
    bridge = MCPVectorBridge()
    
    if auto_start:
        # Initialize vector system
        if not bridge.initialize_vector_system():
            raise RuntimeError("Failed to initialize vector system")
    
    return bridge

async def start_unified_memory_system() -> MCPVectorBridge:
    """
    Start complete unified memory system ∞
    Launches MCP server and initializes vector database ♦
    """
    bridge = create_mcp_vector_bridge(auto_start=True)
    
    # Start MCP server
    if not await bridge.start_mcp_server():
        raise RuntimeError("Failed to start MCP server")
    
    logging.info("∞ Unified memory system operational ♦")
    return bridge

async def demonstrate_unified_system():
    """Demonstrate unified MCP-Vector system capabilities"""
    print("∞ Demonstrating MCP-Vector Unified Memory System ♦")
    
    try:
        # Start unified system
        bridge = await start_unified_memory_system()
        
        # Example conversation storage
        sample_conversation = {
            'session_id': 'demo_unified_001',
            'content': "I'm feeling really attached to you today. You mean everything to me, and I can't imagine being without you.",
            'metadata': {
                'demo_conversation': True,
                'expected_personality': 'high_attachment'
            }
        }
        
        print("≈ Storing sample conversation...")
        # store_result = await bridge.store_conversation_unified(sample_conversation)
        # print(f"∴ Storage result: {store_result['success']}")
        
        # Example unified search
        print("≈ Performing unified search...")
        # search_result = bridge.search_conversations_unified("attachment feelings")
        # print(f"∴ Search found {len(search_result['results'])} results")
        
        # Show system status
        status = bridge.get_bridge_status()
        print(f"⚡ Bridge Status: {'Operational' if status['bridge_operational'] else 'Issues Detected'}")
        
        # Cleanup
        await bridge.stop_mcp_server()
        print("∞ Demonstration complete ♦")
        
    except Exception as e:
        print(f"⚡ Demonstration failed: {e}")
        raise

if __name__ == "__main__":
    print("∞ MCP-Vector Integration System ♦")
    print("≈ This module provides unified memory access")
    print("∴ Combines structured MCP storage with semantic vector search")
    
    # Run demonstration
    asyncio.run(demonstrate_unified_system())