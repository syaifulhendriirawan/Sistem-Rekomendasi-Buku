/**
 * BookCard Component
 * Displays a book with cover image and title
 */
import './BookCard.css';
import { PLACEHOLDER_IMAGE } from '../../lib/constants';

function BookCard({ title, imageUrl, distance, onClick, isSelected = false }) {
    const handleImageError = (e) => {
        e.target.src = PLACEHOLDER_IMAGE;
    };

    return (
        <article
            className={`book-card ${isSelected ? 'book-card--selected' : ''} ${onClick ? 'book-card--clickable' : ''}`}
            onClick={onClick}
        >
            <div className="book-card__cover">
                <img
                    src={imageUrl || PLACEHOLDER_IMAGE}
                    alt={`Cover of ${title}`}
                    onError={handleImageError}
                    loading="lazy"
                />
                {distance !== undefined && (
                    <span className="book-card__similarity">
                        {Math.round((1 - distance) * 100)}% match
                    </span>
                )}
            </div>
            <div className="book-card__info">
                <h3 className="book-card__title" title={title}>
                    {title}
                </h3>
            </div>
        </article>
    );
}

export default BookCard;
