#!/usr/bin/env python3
"""
COVID-19 News Text Extraction Script
Extracts text content from web pages, specifically designed for UNAM Global and other news sources.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import re
from urllib.parse import urljoin, urlparse
from datetime import datetime
import logging
import os
from typing import Dict, List, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NewsTextExtractor:
    """Extract text content from news websites"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        # Try multiple selectors for title
        title_selectors = [
            'h1.page-title',
            'h1.entry-title',
            'h1.post-title',
            'h1.article-title',
            'h1',
            'title'
        ]
        
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem and title_elem.get_text().strip():
                return title_elem.get_text().strip()
        
        return "No title found"
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main article content"""
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        # Try multiple selectors for main content
        content_selectors = [
            'main#primary',
            'article .entry-content',
            'article .post-content',
            'article .article-content',
            '.entry-content',
            '.post-content',
            '.article-content',
            'article',
            '.content',
            'main'
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                return content_elem.get_text()
        
        return soup.get_text()
    
    def _extract_articles_from_archive(self, soup: BeautifulSoup) -> str:
        """Extract all articles from an archive page"""
        articles_text = []
        
        # Find all article elements
        articles = soup.find_all('article')
        
        for i, article in enumerate(articles, 1):
            # Extract title
            title_elem = article.find('h2', class_='entry-title')
            if not title_elem:
                continue
                
            title = title_elem.get_text().strip()
            articles_text.append(f"\n=== ARTÍCULO {i}: {title} ===\n")
            
            # Extract author
            author_elem = article.find('span', class_='author')
            if author_elem:
                author = author_elem.get_text().strip()
                articles_text.append(f"Autor: {author}\n")
            
            # Extract date
            date_elem = article.find('time', class_='entry-date')
            if date_elem:
                date_text = date_elem.get_text().strip()
                articles_text.append(f"Fecha: {date_text}\n")
            
            # Extract categories
            cat_elem = article.find('span', class_='cat-links')
            if cat_elem:
                categories = cat_elem.get_text().strip()
                articles_text.append(f"Categorías: {categories}\n")
            
            articles_text.append("\n--- CONTENIDO ---\n")
            
            # Extract content
            content_elem = article.find('div', class_='entry-content')
            if content_elem:
                content = content_elem.get_text().strip()
                articles_text.append(content)
            
            articles_text.append("\n" + "="*80 + "\n")
        
        return "\n".join(articles_text)
    
        """
        Extract all article content from HTML and return as list of strings
        
        Args:
            html_content: Raw HTML content as string
            
        Returns:
            List of strings, each containing one article's content
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []
        
        # Find all article elements
        article_elements = soup.find_all('article')
        
        for article in article_elements:
            # Get the text content of each article
            article_text = article.get_text()
            # Clean the text
            cleaned_text = self._clean_text(article_text)
            if cleaned_text.strip():  # Only add non-empty articles
                articles.append(cleaned_text)
        
        return articles
    
        """
        Extract all articles from HTML with metadata and return as list of dictionaries
        
        Args:
            html_content: Raw HTML content as string
            
        Returns:
            List of dictionaries, each containing article data
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []
        
        # Find all article elements
        article_elements = soup.find_all('article')
        
        for i, article in enumerate(article_elements, 1):
            # Extract title
            title_elem = article.find('h2', class_='entry-title')
            title = title_elem.get_text().strip() if title_elem else f"Article {i}"
            
            # Extract author
            author_elem = article.find('span', class_='author')
            author = author_elem.get_text().strip() if author_elem else "Unknown"
            
            # Extract date
            date_elem = article.find('time', class_='entry-date')
            date = date_elem.get_text().strip() if date_elem else "Unknown"
            
            # Extract categories
            cat_elem = article.find('span', class_='cat-links')
            categories = cat_elem.get_text().strip() if cat_elem else "Unknown"
            
            # Extract content
            content_elem = article.find('div', class_='entry-content')
            if content_elem:
                content = content_elem.get_text()
                cleaned_content = self._clean_text(content)
            else:
                cleaned_content = self._clean_text(article.get_text())
            
            if cleaned_content.strip():  # Only add non-empty articles
                articles.append({
                    'article_number': i,
                    'title': title,
                    'author': author,
                    'date': date,
                    'categories': categories,
                    'content': cleaned_content,
                    'word_count': len(cleaned_content.split())
                })
        
        return articles
    
    def _extract_author(self, soup: BeautifulSoup) -> str:
        """Extract article author"""
        author_selectors = [
            'span.author.vcard',
            '.entry-author',
            '.post-author',
            '.article-author',
            '.author',
            'meta[name="author"]'
        ]
        
        for selector in author_selectors:
            author_elem = soup.select_one(selector)
            if author_elem:
                if author_elem.get('content'):
                    return author_elem.get('content')
                return author_elem.get_text().strip()
        
        return "No author found"
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text for LLM processing"""
        if not text:
            return ""
        
        # Remove HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#8217;', "'")
        text = text.replace('&#8220;', '"')
        text = text.replace('&#8221;', '"')
        text = text.replace('&#8230;', '...')
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common unwanted patterns
        text = re.sub(r'Share this:', '', text)
        text = re.sub(r'Like this:', '', text)
        text = re.sub(r'Posted in.*?Tagged.*?$', '', text, flags=re.MULTILINE | re.DOTALL)
        text = re.sub(r'Posted in.*?$', '', text, flags=re.MULTILINE)
        text = re.sub(r'Tagged.*?$', '', text, flags=re.MULTILINE)
        
        # Remove navigation and footer content
        text = re.sub(r'Entradas anteriores.*?$', '', text, flags=re.MULTILINE | re.DOTALL)
        text = re.sub(r'Buscar:.*?$', '', text, flags=re.MULTILINE | re.DOTALL)
        text = re.sub(r'Relevante.*?$', '', text, flags=re.MULTILINE | re.DOTALL)
        text = re.sub(r'Comentarios recientes.*?$', '', text, flags=re.MULTILINE | re.DOTALL)
        text = re.sub(r'Archivos.*?$', '', text, flags=re.MULTILINE | re.DOTALL)
        text = re.sub(r'Meta.*?$', '', text, flags=re.MULTILINE | re.DOTALL)
        text = re.sub(r'Acerca de nosotros.*?$', '', text, flags=re.MULTILINE | re.DOTALL)
        
        # Remove social media and sharing buttons
        text = re.sub(r'Facebook.*?$', '', text, flags=re.MULTILINE)
        text = re.sub(r'YouTube.*?$', '', text, flags=re.MULTILINE)
        text = re.sub(r'Twitter.*?$', '', text, flags=re.MULTILINE)
        text = re.sub(r'SoundCloud.*?$', '', text, flags=re.MULTILINE)
        
        # Remove WordPress-specific content
        text = re.sub(r'Posted on.*?by.*?$', '', text, flags=re.MULTILINE)
        text = re.sub(r'Posted in.*?$', '', text, flags=re.MULTILINE)
        text = re.sub(r'Posted by.*?$', '', text, flags=re.MULTILINE)
        
        # Remove iframe content references
        text = re.sub(r'iframe.*?src=.*?$', '', text, flags=re.MULTILINE | re.DOTALL)
        
        # Remove language-specific span tags content (keep only the text)
        text = re.sub(r'<span lang="[^"]*">', '', text)
        text = re.sub(r'</span>', '', text)
        
        # Remove empty paragraphs and extra spaces
        text = re.sub(r'<p><span lang="[^"]*">\s*</span></p>', '', text)
        text = re.sub(r'<p>\s*</p>', '', text)
        
        # Remove bold tags but keep content
        text = re.sub(r'<b>', '', text)
        text = re.sub(r'</b>', '', text)
        
        # Remove paragraph tags but keep line breaks
        text = re.sub(r'<p>', '\n', text)
        text = re.sub(r'</p>', '', text)
        
        # Clean up line breaks and spaces
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'^\s+|\s+$', '', text, flags=re.MULTILINE)
        text = text.strip()
        
        return text
    
    def extract_from_unam_global(self, year: int = 2020, month: int = 1) -> Dict:
        """
        Extract main content from UNAM Global monthly archive page
        
        Args:
            year: Year to extract (default: 2020)
            month: Month to extract (default: 1 for January)
            
        Returns:
            Dictionary with extracted content from the main page
        """
        base_url = f"https://unamglobal.unam.mx/{year:04d}/{month:02d}/"
        logger.info(f"Extracting from UNAM Global: {base_url}")
        
        try:
            response = self.session.get(base_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to extract articles from archive page first
            articles_content = self._extract_articles_from_archive(soup)
            content = ''
            if articles_content.strip():
                content = articles_content
            
            return {
                'content': content,
                'word_count': len(content.split()),
                'extraction_date': datetime.now().isoformat(),
            }
            
        except Exception as e:
            logger.error(f"Error extracting from UNAM Global: {str(e)}")
            return {
                'url': base_url,
                'error': str(e),
                'extraction_date': datetime.now().isoformat()
            }
    
    def save_to_txt(self, article: Dict, year: int, month: int):
        """Save extracted article to clean text file for LLM processing"""
        # Create filename with month and year
        month_names = {
            1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
            7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
        }
        month_name = month_names.get(month, f"mes_{month}")
        filename = f"../data/text/{month}_{year}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            if 'error' in article:
                f.write(f"Error: {article.get('error', 'Unknown error')}\n")
            else:
                # Count articles in content
                content = article.get('content', '')
                article_count = content.count('=== ARTÍCULO')
                f.write(content)
        
        logger.info(f"Saved article to {filename} (Found {article_count} articles)")
    

def main():
    """Main function to run the text extraction from January 2020 to December 2023"""
    extractor = NewsTextExtractor()
    
    # Define the date range
    start_year = 2020
    end_year = 2023
    
    # Month names for display
    month_names = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
        7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }
    
    total_articles = 0
    successful_extractions = 0
    failed_extractions = 0
    
    print(f"Starting COVID-19 news extraction from UNAM Global ({month_names[1]} {start_year} to {month_names[12]} {end_year})")
    print("=" * 80)
    
    # Loop through all years and months
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            print(f"\nExtracting COVID-19 news from UNAM Global ({month} {year})...")
            
            try:
                article = extractor.extract_from_unam_global(year=year, month=month)
                
                if 'error' not in article:
                    word_count = article.get('word_count', 0)
                    print(f"✓ Successfully extracted content from UNAM Global")
                    print(f"  Word Count: {word_count}")
                    
                    # Save to clean text file for LLM processing
                    extractor.save_to_txt(article, year=year, month=month)
                    print(f"  Content saved to: ../data/text/{month}_{year}.txt")
                    
                    successful_extractions += 1
                    total_articles += word_count
                else:
                    print(f"✗ Error extracting content: {article.get('error', 'Unknown error')}")
                    failed_extractions += 1
                    
            except Exception as e:
                print(f"✗ Exception during extraction: {str(e)}")
                failed_extractions += 1
            
            # Add a small delay to be respectful to the server
            time.sleep(1)
    
    # Print summary
    print("\n" + "=" * 80)
    print("EXTRACTION SUMMARY")
    print("=" * 80)
    print(f"Total months processed: {(end_year - start_year + 1) * 12}")
    print(f"Successful extractions: {successful_extractions}")
    print(f"Failed extractions: {failed_extractions}")
    print(f"Total words extracted: {total_articles:,}")
    print(f"Success rate: {(successful_extractions / ((end_year - start_year + 1) * 12)) * 100:.1f}%")

if __name__ == "__main__":
    main()
