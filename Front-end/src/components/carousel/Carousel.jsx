import './Carousel.css';

import {useEffect, useRef, useState} from 'react';


export default function CarouselComponent({data}) {
    const [activeIndex, setActiveIndex] = useState(0);
    data = items;
    return (
        <>
            <Carousel activeIndex={activeIndex} setActiveIndex={setActiveIndex}>
                {data.map((card, i) => {
                    return (
                        <CarouselCard key={card.imageId} active={activeIndex === i}>
                            <img className='carousel-card-content' src = {card.url} alt={card.name}/>
                        </CarouselCard>
                    )
                })}
            </Carousel>
            <div className="button-group">
                <button type="button" disabled={activeIndex === 0} onClick={() => setActiveIndex(activeIndex - 1)}>Prev</button>
                <button type="button" disabled={activeIndex === data.length - 1} onClick={() => setActiveIndex(activeIndex + 1)}>Next</button>
            </div>
        </>
    )
}
let sizeFactor = 4;

function Carousel ({activeIndex, setActiveIndex, children}) {
    const carouselRef = useRef(null);
    const [carouselTranslate, setCarouselTranslate] = useState(null);

    useEffect(() => {
        console.log(activeIndex)
        const initialTranslateVal = carouselRef.current.offsetWidth / 4;
        const translate = activeIndex === 0 ? initialTranslateVal : initialTranslateVal - (activeIndex * initialTranslateVal);
        setCarouselTranslate(translate);
    }, [activeIndex]);

    return (
        <>
            <div className="carousel" ref={carouselRef} style={{transform: `translateX(${carouselTranslate}px)`}}>
                {children}
            </div>
            <div className="dots">
                {children.map((child, i) => <button className={`dot ${activeIndex === i ? 'active' : ''}`} onClick={() => setActiveIndex(i)}/>)}
            </div>
        </>
    )
}

function CarouselCard ({active, children}) {
    return (
        <div className={`carousel-card ${active ? 'active' : ''}`} style={{width: `${100/sizeFactor}%`}}>
            {children}
        </div>
    )
}

const items = [
    {
        name: 'One',
        imageId: '1bX5QH6',
        url: `/img/coworking-colleagues-having-conversation-at-workplace.jpg`
    },
    {
        name: 'Two',
        imageId: '2',
        url: `/img/coworking-workplace-interior.jpg`
    },
    {
        name: 'Three',
        imageId: '3',
        url: `/img/people-working-in-modern-co-working-space.jpg`
    },
    {
        name: 'Four',
        imageId: '4',
        url: `/img/puestos-flexibles-coworking.webp`
    },
]
