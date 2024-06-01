import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import AboutUs from "./components/AboutUs";
import ContactUs from "./components/ContactUs";
import HomePage from "./components/HomePage";
import Navbar from "./components/Navbar";
import Predict from "./components/Predict";
import Services from "./components/Services";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={
          <>
            <section id="home">
              <HomePage />
            </section>
            <section id="services">
              <Services />
            </section>
            <section id="about">
              <AboutUs />
            </section>
            <section id="contact">
              <ContactUs />
            </section>
          </>
        } />
        <Route path="/caption" element={<Predict/>} />
      </Routes>
    </Router>
  );
}

export default App;