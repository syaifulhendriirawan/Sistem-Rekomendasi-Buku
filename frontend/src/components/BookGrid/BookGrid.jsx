/**
 * BookGrid Component
 * Displays a grid of BookCards
 */
import './BookGrid.css';
import BookCard from '../BookCard';

function BookGrid({ books, onBookClick, selectedBook, showSimilarity = false }) {
    if (!books || books.length === 0) {
        return null;
    }

    return (
        <div className="book-grid">
            {books.map((book, index) => (
                <BookCard
                    key={`${book.title}-${index}`}
                    title={book.title}
                    imageUrl={book.image_url}
                    distance={showSimilarity ? book.distance : undefined}
                    isSelected={selectedBook === book.title}
                    onClick={onBookClick ? () => onBookClick(book.title) : undefined}
                />
            ))}
        </div>
    );
}

export default BookGrid;
