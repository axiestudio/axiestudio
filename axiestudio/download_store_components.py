#!/usr/bin/env python3
"""
Langflow Store Components Downloader for Axie Studio
Downloads all components from the Langflow Store and saves them locally.
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict, List

import httpx
from loguru import logger

# Langflow Store Configuration
STORE_BASE_URL = "https://www.langflow.store"
STORE_API_KEY = "yl0fxKXHcPGa_LVbSD3opKxgi_nKqL-7"
COMPONENTS_URL = f"{STORE_BASE_URL}/items/components"
DOWNLOAD_DIR = Path("src/store_components")

# Default fields to fetch
DEFAULT_FIELDS = [
    "id",
    "name", 
    "description",
    "user_created.username",
    "is_component",
    "tags.tags_id.name",
    "tags.tags_id.id",
    "count(liked_by)",
    "count(downloads)",
    "metadata",
    "last_tested_version",
    "private",
    "data"  # This contains the actual flow/component data
]


class LangflowStoreDownloader:
    """Downloads components from the Langflow Store."""
    
    def __init__(self):
        self.base_url = STORE_BASE_URL
        self.api_key = STORE_API_KEY
        self.components_url = COMPONENTS_URL
        self.download_dir = DOWNLOAD_DIR
        self.timeout = 30
        
        # Create download directory
        self.download_dir.mkdir(parents=True, exist_ok=True)
        
    async def get_components(
        self, 
        page: int = 1, 
        limit: int = 100,
        fields: List[str] = None
    ) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Fetch components from the store."""
        
        if fields is None:
            fields = DEFAULT_FIELDS
            
        params = {
            "page": page,
            "limit": limit,
            "fields": ",".join(fields),
            "meta": "filter_count",
        }
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        async with httpx.AsyncClient() as client:
            try:
                logger.info(f"Fetching page {page} with limit {limit}")
                response = await client.get(
                    self.components_url, 
                    headers=headers, 
                    params=params, 
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                json_response = response.json()
                result = json_response.get("data", [])
                metadata = json_response.get("meta", {})
                
                logger.info(f"Fetched {len(result)} components from page {page}")
                return result, metadata
                
            except Exception as exc:
                logger.error(f"Failed to fetch components: {exc}")
                raise
    
    async def download_all_components(self) -> List[Dict[str, Any]]:
        """Download all components from all pages."""
        all_components = []
        page = 1
        limit = 100
        
        while True:
            try:
                components, metadata = await self.get_components(page=page, limit=limit)
                
                if not components:
                    logger.info("No more components to fetch")
                    break
                    
                all_components.extend(components)
                logger.info(f"Total components downloaded: {len(all_components)}")
                
                # Check if we have more pages
                total_count = metadata.get("filter_count", 0)
                if len(all_components) >= total_count:
                    logger.info(f"Downloaded all {total_count} components")
                    break
                    
                page += 1
                
            except Exception as exc:
                logger.error(f"Error downloading page {page}: {exc}")
                break
                
        return all_components
    
    def save_component(self, component: Dict[str, Any]) -> None:
        """Save a single component to disk."""
        try:
            component_id = component.get("id")
            component_name = component.get("name", "unnamed")
            
            # Clean filename
            safe_name = "".join(c for c in component_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{component_id}_{safe_name}.json"
            
            filepath = self.download_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(component, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Saved component: {safe_name} -> {filename}")
            
        except Exception as exc:
            logger.error(f"Failed to save component {component.get('name', 'unknown')}: {exc}")
    
    def save_components_index(self, components: List[Dict[str, Any]]) -> None:
        """Save an index file with all components metadata."""
        try:
            # Create a simplified index for quick browsing
            index = []
            for component in components:
                index_entry = {
                    "id": component.get("id"),
                    "name": component.get("name"),
                    "description": component.get("description"),
                    "is_component": component.get("is_component"),
                    "tags": component.get("tags", []),
                    "downloads": component.get("count(downloads)", 0),
                    "likes": component.get("count(liked_by)", 0),
                    "author": component.get("user_created", {}).get("username", "Unknown"),
                    "last_tested_version": component.get("last_tested_version"),
                }
                index.append(index_entry)
            
            # Sort by downloads (most popular first)
            index.sort(key=lambda x: x.get("downloads", 0), reverse=True)
            
            index_file = self.download_dir / "components_index.json"
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "total_components": len(index),
                    "downloaded_at": str(asyncio.get_event_loop().time()),
                    "components": index
                }, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Saved components index with {len(index)} components")
            
        except Exception as exc:
            logger.error(f"Failed to save components index: {exc}")
    
    async def run(self) -> None:
        """Main download process."""
        logger.info("Starting Langflow Store components download...")
        logger.info(f"Download directory: {self.download_dir.absolute()}")
        
        try:
            # Download all components
            components = await self.download_all_components()
            
            if not components:
                logger.warning("No components downloaded")
                return
            
            logger.info(f"Downloaded {len(components)} components total")
            
            # Save each component
            for component in components:
                self.save_component(component)
            
            # Save index file
            self.save_components_index(components)
            
            logger.info("✅ Download completed successfully!")
            logger.info(f"📁 Components saved to: {self.download_dir.absolute()}")
            
        except Exception as exc:
            logger.error(f"❌ Download failed: {exc}")
            raise


async def main():
    """Main entry point."""
    downloader = LangflowStoreDownloader()
    await downloader.run()


if __name__ == "__main__":
    asyncio.run(main())
