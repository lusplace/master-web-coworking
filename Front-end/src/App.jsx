import Carousel from './components/carousel/carousel';
import FooterComponent from './components/footer/footer';
import Navbar from './components/navbar/NavBar';

function App() {
  return <>
  <Navbar/>
  <h1>hiiiii</h1>
    <DefaultApp/>
      <Carousel/>
    <FooterComponent/>
  </>
}

function DefaultApp(){
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      fontFamily: 'system-ui, -apple-system, sans-serif',
      //backgroundColor: '#f5f5f5'
    }} className='cross'>
      <h1 style={{
        fontSize: '3rem',
        color: '#333',
        marginBottom: '1rem'
      }}>
        Coworking App
      </h1>
      <p style={{
        fontSize: '1.2rem',
        color: '#666',
        textAlign: 'center',
        maxWidth: '600px'
      }}>
        COWORKING PROJECT - MASTER WEB
      </p>
    </div>
  )
}

export default App
