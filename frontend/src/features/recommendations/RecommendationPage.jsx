/**
 * RecommendationPage - Main page for book recommendations
 */
import { useCallback, useEffect } from 'react';
import './RecommendationPage.css';
import useBookStore from '../../stores/useBookStore';
import SearchDropdown from '../../components/SearchDropdown';
import BookGrid from '../../components/BookGrid';
import LoadingSpinner from '../../components/LoadingSpinner';
import BookCarousel from '../../components/BookCarousel';
import BookDetail from '../../components/BookDetail';
import { APP_NAME } from '../../lib/constants';

function RecommendationPage() {
    const {
        searchResults,
        selectedBook,
        selectedBookDetails,
        recommendations,
        featuredBooks,
        isLoading,
        isSearching,
        error,
        searchBooks,
        selectBook,
        clearSelection,
        clearError,
        fetchFeaturedBooks,
    } = useBookStore();

    useEffect(() => {
        fetchFeaturedBooks();
    }, [fetchFeaturedBooks]);

    const handleSearch = useCallback((query) => {
        searchBooks(query);
    }, [searchBooks]);

    const handleSelect = useCallback((bookTitle) => {
        selectBook(bookTitle);
        // Scroll to details is handled automatically or we can force it
        setTimeout(() => {
            document.getElementById('book-detail')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
    }, [selectBook]);

    return (
        <div className="recommendation-page">
            {/* Navigation / Header */}
            {/* Navigation / Header */}
            <nav className="navbar">
                <div className="navbar__container">
                    {/* Empty or minimalistic menu if needed later */}
                </div>
            </nav>

            {/* Hero Section */}
            <header className="hero">
                <div className="hero__content">
                    <h1 className="hero__title">
                        Find your next favorite story.
                    </h1>
                    <p className="hero__description">
                        Explore our curated collection of trending titles and hidden gems selected just for you.
                    </p>

                    <div className="hero__search-container">
                        <SearchDropdown
                            books={searchResults}
                            onSearch={handleSearch}
                            onSelect={handleSelect}
                            isSearching={isSearching}
                            placeholder="Search by title..."
                        />
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="main-content">
                {/* Error State */}
                {error && (
                    <div className="error-banner">
                        <p>{error}</p>
                        <button onClick={clearError} className="error-banner__close">✕</button>
                    </div>
                )}

                {selectedBook ? (
                    <div id="book-detail">
                        {isLoading && !selectedBookDetails ? (
                            <div className="loading-container">
                                <LoadingSpinner size="large" text="Fetching book details..." />
                            </div>
                        ) : selectedBookDetails && (
                            <section className="detail-section">
                                <BookDetail
                                    book={selectedBookDetails}
                                    onClose={clearSelection}
                                />

                                {recommendations.length > 0 && (
                                    <div className="recommendations-container">
                                        <h3 className="section-title">You might also like</h3>
                                        <p className="section-subtitle">Based on similarity to "{selectedBookDetails.title}"</p>
                                        <div className="spacer"></div>
                                        <BookGrid
                                            books={recommendations}
                                            showSimilarity={true}
                                            onBookClick={handleSelect}
                                        />
                                    </div>
                                )}
                            </section>
                        )}
                    </div>
                ) : (
                    /* Featured Carousel (Default View) */
                    <section className="featured-section">
                        <div className="section-header">
                            <h2 className="section-title">Trending Books</h2>
                            <p className="section-subtitle">Most popular reads this week</p>
                        </div>

                        {featuredBooks.length > 0 ? (
                            <div className="featured-grid-wrapper">
                                <BookCarousel
                                    books={featuredBooks}
                                    onBookClick={handleSelect}
                                />
                            </div>
                        ) : (
                            <div className="loading-container">
                                <LoadingSpinner text="Loading library..." />
                            </div>
                        )}
                    </section>
                )}
            </main>

            {/* Footer */}
            <footer className="footer">
                <p>
                    Built with <span className="heart">❤</span> for book lovers
                </p>
                <p className="footer__tech">
                    Boo RecommenderAI • 270K+ Books
                </p>
            </footer>
        </div>
    );
}

export default RecommendationPage;
