/**
 * Zustand store for book recommendation state
 */
import { create } from 'zustand';
import api from '../lib/api';

const useBookStore = create((set, get) => ({
    // State
    books: [],
    selectedBook: null,
    recommendations: [],
    searchResults: [],
    isLoading: false,
    isSearching: false,
    error: null,

    // Actions

    /**
     * Fetch all available books
     */
    fetchBooks: async () => {
        set({ isLoading: true, error: null });
        try {
            const books = await api.getBooks();
            set({ books, isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    /**
     * Search books by query
     */
    searchBooks: async (query) => {
        if (!query || query.length < 2) {
            set({ searchResults: [] });
            return;
        }

        set({ isSearching: true });
        try {
            const results = await api.searchBooks(query, 20);
            set({ searchResults: results, isSearching: false });
        } catch (error) {
            set({ searchResults: [], isSearching: false });
        }
    },

    /**
     * Select a book and get recommendations
     */
    selectBook: async (bookTitle) => {
        set({
            selectedBook: bookTitle,
            isLoading: true,
            error: null,
            recommendations: [],
            searchResults: []
        });

        try {
            const response = await api.getRecommendations(bookTitle, 5);
            set({
                recommendations: response.recommendations,
                isLoading: false
            });
        } catch (error) {
            set({
                error: error.message,
                isLoading: false,
                recommendations: []
            });
        }
    },

    /**
     * Clear current selection
     */
    clearSelection: () => {
        set({
            selectedBook: null,
            recommendations: [],
            error: null,
            searchResults: []
        });
    },

    /**
     * Clear error
     */
    clearError: () => {
        set({ error: null });
    },
}));

export default useBookStore;
