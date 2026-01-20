/**
 * SearchDropdown Component
 * Autocomplete search for books with debounced input
 */
import { useState, useEffect, useRef, useCallback } from 'react';
import './SearchDropdown.css';

function SearchDropdown({
    books = [],
    onSearch,
    onSelect,
    isSearching = false,
    placeholder = "Search for a book..."
}) {
    const [query, setQuery] = useState('');
    const [isOpen, setIsOpen] = useState(false);
    const [highlightedIndex, setHighlightedIndex] = useState(-1);
    const inputRef = useRef(null);
    const dropdownRef = useRef(null);
    const debounceRef = useRef(null);

    // Debounced search
    useEffect(() => {
        if (debounceRef.current) {
            clearTimeout(debounceRef.current);
        }

        if (query.length >= 2) {
            debounceRef.current = setTimeout(() => {
                onSearch?.(query);
                setIsOpen(true);
            }, 300);
        } else {
            setIsOpen(false);
        }

        return () => {
            if (debounceRef.current) {
                clearTimeout(debounceRef.current);
            }
        };
    }, [query, onSearch]);

    // Close dropdown on outside click
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const handleSelect = useCallback((book) => {
        setQuery(book);
        setIsOpen(false);
        setHighlightedIndex(-1);
        onSelect?.(book);
    }, [onSelect]);

    const handleKeyDown = (e) => {
        if (!isOpen || books.length === 0) return;

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                setHighlightedIndex((prev) =>
                    prev < books.length - 1 ? prev + 1 : 0
                );
                break;
            case 'ArrowUp':
                e.preventDefault();
                setHighlightedIndex((prev) =>
                    prev > 0 ? prev - 1 : books.length - 1
                );
                break;
            case 'Enter':
                e.preventDefault();
                if (highlightedIndex >= 0) {
                    handleSelect(books[highlightedIndex]);
                }
                break;
            case 'Escape':
                setIsOpen(false);
                setHighlightedIndex(-1);
                break;
        }
    };

    return (
        <div className="search-dropdown" ref={dropdownRef}>
            <div className="search-dropdown__input-wrapper">
                <svg
                    className="search-dropdown__icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                >
                    <circle cx="11" cy="11" r="8" />
                    <path d="M21 21l-4.35-4.35" />
                </svg>
                <input
                    ref={inputRef}
                    type="text"
                    className="search-dropdown__input"
                    placeholder={placeholder}
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={handleKeyDown}
                    onFocus={() => query.length >= 2 && books.length > 0 && setIsOpen(true)}
                    aria-label="Search books"
                    aria-autocomplete="list"
                    aria-expanded={isOpen}
                />
                {isSearching && (
                    <div className="search-dropdown__spinner" />
                )}
            </div>

            {isOpen && books.length > 0 && (
                <ul className="search-dropdown__list" role="listbox">
                    {books.map((book, index) => (
                        <li
                            key={`${book}-${index}`}
                            className={`search-dropdown__item ${index === highlightedIndex ? 'search-dropdown__item--highlighted' : ''
                                }`}
                            onClick={() => handleSelect(book)}
                            onMouseEnter={() => setHighlightedIndex(index)}
                            role="option"
                            aria-selected={index === highlightedIndex}
                        >
                            {book}
                        </li>
                    ))}
                </ul>
            )}

            {isOpen && query.length >= 2 && books.length === 0 && !isSearching && (
                <div className="search-dropdown__empty">
                    No books found matching "{query}"
                </div>
            )}
        </div>
    );
}

export default SearchDropdown;
