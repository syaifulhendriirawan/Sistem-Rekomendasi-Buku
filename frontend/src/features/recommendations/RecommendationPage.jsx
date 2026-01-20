/**
 * RecommendationPage - Main page for book recommendations
 */
import { useCallback } from 'react';
import './RecommendationPage.css';
import useBookStore from '../../stores/useBookStore';
import SearchDropdown from '../../components/SearchDropdown';
import BookGrid from '../../components/BookGrid';
import LoadingSpinner from '../../components/LoadingSpinner';
import { APP_NAME, APP_DESCRIPTION } from '../../lib/constants';

function RecommendationPage() {
    const {
        searchResults,
        selectedBook,
        recommendations,
        isLoading,
        isSearching,
        error,
        searchBooks,
        selectBook,
        clearSelection,
        clearError,
    } = useBookStore();

    const handleSearch = useCallback((query) => {
        searchBooks(query);
    }, [searchBooks]);

    const handleSelect = useCallback((bookTitle) => {
        selectBook(bookTitle);
    }, [selectBook]);

    return (
        <div className="recommendation-page">
            {/* Hero Section */}
            <header className="hero">
                <div className="hero__background">
                    <div className="hero__gradient" />
                    <div className="hero__pattern" />
                </div>

                <div className="hero__content">
                    <h1 className="hero__title">
                        <span className="hero__emoji">📚</span>
                        {APP_NAME}
                    </h1>
                    <p className="hero__description">{APP_DESCRIPTION}</p>

                    <SearchDropdown
                        books={searchResults}
                        onSearch={handleSearch}
                        onSelect={handleSelect}
                        isSearching={isSearching}
                        placeholder="Type a book title to find recommendations..."
                    />
                </div>
            </header>

            {/* Main Content */}
            <main className="main-content">
                {/* Error State */}
                {error && (
                    <div className="error-banner">
                        <p>{error}</p>
                        <button onClick={clearError} className="error-banner__close">
                            ✕
                        </button>
                    </div>
                )}

                {/* Loading State */}
                {isLoading && (
                    <div className="loading-container">
                        <LoadingSpinner size="large" text="Finding similar books..." />
                    </div>
                )}

                {/* Results */}
                {!isLoading && selectedBook && recommendations.length > 0 && (
                    <section className="results-section">
                        <div className="results-header">
                            <h2 className="results-title">
                                Because you liked <span className="highlight">"{selectedBook}"</span>
                            </h2>
                            <button onClick={clearSelection} className="btn btn--ghost">
                                Clear Selection
                            </button>
                        </div>

                        <BookGrid
                            books={recommendations}
                            showSimilarity={true}
                        />
                    </section>
                )}

                {/* Empty State */}
                {!isLoading && !selectedBook && (
                    <section className="empty-state">
                        <div className="empty-state__icon">🔍</div>
                        <h2 className="empty-state__title">Start by searching for a book</h2>
                        <p className="empty-state__text">
                            Our AI-powered system uses collaborative filtering to find books
                            that readers with similar tastes enjoyed.
                        </p>

                        <div className="features">
                            <div className="feature">
                                <span className="feature__icon">⚡</span>
                                <h3 className="feature__title">Fast Results</h3>
                                <p className="feature__text">Get recommendations in under 50ms</p>
                            </div>
                            <div className="feature">
                                <span className="feature__icon">🎯</span>
                                <h3 className="feature__title">Accurate Matching</h3>
                                <p className="feature__text">Based on 1M+ user ratings</p>
                            </div>
                            <div className="feature">
                                <span className="feature__icon">🤖</span>
                                <h3 className="feature__title">Smart Algorithm</h3>
                                <p className="feature__text">KNN with cosine similarity</p>
                            </div>
                        </div>
                    </section>
                )}
            </main>

            {/* Footer */}
            <footer className="footer">
                <p>
                    Built with <span className="heart">❤</span> using React + FastAPI
                </p>
                <p className="footer__tech">
                    Collaborative Filtering • K-Nearest Neighbors • 270K+ Books
                </p>
            </footer>
        </div>
    );
}

export default RecommendationPage;
