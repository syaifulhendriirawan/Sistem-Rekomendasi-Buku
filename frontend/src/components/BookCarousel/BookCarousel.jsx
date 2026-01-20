/**
 * BookCarousel Component
 * Displays a swipeable list of books
 */
import { Swiper, SwiperSlide } from 'swiper/react';
import { EffectCoverflow, Pagination, Navigation, Autoplay } from 'swiper/modules';
import BookCard from '../BookCard';

// Import Swiper styles
import 'swiper/css';
import 'swiper/css/effect-coverflow';
import 'swiper/css/pagination';
import 'swiper/css/navigation';
import './BookCarousel.css';

function BookCarousel({ books, onBookClick }) {
    if (!books || books.length === 0) return null;

    return (
        <div className="book-carousel">
            <Swiper
                effect={'coverflow'}
                grabCursor={true}
                centeredSlides={true}
                slidesPerView={'auto'}
                coverflowEffect={{
                    rotate: 0,
                    stretch: 0,
                    depth: 100,
                    modifier: 2.5,
                    slideShadows: false,
                }}
                pagination={{ clickable: true }}
                navigation={true}
                loop={true}
                autoplay={{
                    delay: 3000,
                    disableOnInteraction: false,
                    pauseOnMouseEnter: true
                }}
                modules={[EffectCoverflow, Pagination, Navigation, Autoplay]}
                className="mySwiper"
            >
                {books.map((book, index) => (
                    <SwiperSlide key={`${book.title}-${index}`}>
                        <BookCard
                            title={book.title}
                            imageUrl={book.image_url}
                            author={book.author}
                            onClick={() => onBookClick(book.title)}
                        />
                    </SwiperSlide>
                ))}
            </Swiper>
        </div>
    );
}

export default BookCarousel;
