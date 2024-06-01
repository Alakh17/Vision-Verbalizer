import { Link } from 'react-router-dom';

function Services() {
  return (
    <div className="bg-gray-100 min-h-screen flex flex-col items-center justify-center py-16">
      <h1 className="text-5xl md:text-6xl font-bold text-blue-700 mb-16">Our Services</h1>
      <div className="w-3/4 md:w-1/3 items-center flex justify-center">
        <div className="bg-white flex w-full flex-col py-10 px-4 justify-center items-center shadow-md rounded-lg text-center transform transition-transform duration-300 hover:scale-105 hover:-translate-y-2">
          <h2 className="text-4xl md:text-3xl font-bold mb-4">Image to Caption Generator</h2>
          <p className="mb-6">Generate the Best Captions for your Image, Uplaod the image and our website will explain your image in words!</p>
          <Link to="/caption" className="bg-blue-700 text-white px-4 py-2 rounded-full text-lg font-semibold transform transition-transform duration-300 hover:scale-105 hover:-translate-y-1">
            Learn More
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Services;