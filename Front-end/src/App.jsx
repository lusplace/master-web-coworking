import FooterComponent from './components/footer/footer';
import Navbar from './components/navbar/NavBar';
import {DefaultApp} from "./components/DefaultApp.jsx";
import CarouselComponent from "./components/carousel/Carousel.jsx";

function App() {
  return <>
  <Navbar/>
    <DefaultApp/>
      <CarouselComponent/>

    <FooterComponent/>
  </>
}



export default App
