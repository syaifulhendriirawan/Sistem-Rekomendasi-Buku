/**
 * BookDetail Component
 * Displays detailed information about a selected book
 */
import './BookDetail.css';

function BookDetail({ book, onClose }) {
    if (!book) return null;

    return (
        <div className="book-detail">
            <button className="book-detail__close" onClick={onClose} aria-label="Close details">
                ✕
            </button>

            <div className="book-detail__content">
                <div className="book-detail__cover-container">
                    <img
                        src={book.image_url}
                        alt={book.title}
                        className="book-detail__cover"
                        onError={(e) => {
                            e.target.src = 'https://via.placeholder.com/300x450?text=No+Cover';
                        }}
                    />
                </div>

                <div className="book-detail__info">
                    <h1 className="book-detail__title">{book.title}</h1>
                    <h2 className="book-detail__author">by {book.author}</h2>

                    <div className="book-detail__meta">
                        <span className="book-detail__meta-item">
                            Published in {book.year > 0 ? book.year : 'Unknown Year'}
                        </span>
                        <span className="book-detail__separator">•</span>
                        <span className="book-detail__meta-item">
                            {book.publisher}
                        </span>
                    </div>

                    <div className="book-detail__description">
                        <p>
                            Discover this compelling story by {book.author}.
                            A perfect choice for readers who enjoy exploring
                            new worlds and engaging narratives.
                            {/* Placeholder description as we don't have real ones */}
                        </p>
                    </div>

                    <div className="book-detail__actions">
                        <button className="btn btn--primary">
                            Find Online
                        </button>
                        <button className="btn btn--secondary">
                            Add to List
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default BookDetail;
