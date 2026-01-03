import { useNavigate } from "react-router-dom";
import { useBooking } from "../context/BookingContext";
import { useState } from "react";

export function InfoPage() {
  const navigate = useNavigate();
  const { selectedEvent, setUserInfo } = useBooking();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");

  if (!selectedEvent) {
    navigate("/home");
    return null;
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setUserInfo({ name, email, phone });
    navigate("/seat");
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl text-purple-600">Ticket Booking</h1>
          <button
            onClick={() => navigate("/home")}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
          >
            ← Back to Events
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-md overflow-hidden mb-8">
          <img
            src={selectedEvent.image}
            alt={selectedEvent.title}
            className="w-full h-64 object-cover"
          />
          <div className="p-6">
            <div className="mb-4">
              <span className="text-xs px-3 py-1 bg-purple-100 text-purple-700 rounded">
                {selectedEvent.category}
              </span>
            </div>
            <h2 className="text-3xl mb-4">{selectedEvent.title}</h2>
            <div className="grid grid-cols-2 gap-4 text-gray-700 mb-6">
              <div>
                <p className="text-sm text-gray-500 mb-1">Date</p>
                <p>{new Date(selectedEvent.date).toLocaleDateString()}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500 mb-1">Time</p>
                <p>{selectedEvent.time}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500 mb-1">Venue</p>
                <p>{selectedEvent.venue}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500 mb-1">Price</p>
                <p className="text-purple-600">${selectedEvent.price}</p>
              </div>
            </div>
            <div className="border-t pt-4">
              <h3 className="mb-2">About This Event</h3>
              <p className="text-gray-600 text-sm">
                Join us for an unforgettable experience at {selectedEvent.title}
                . This event promises to deliver entertainment, excitement, and
                memories that will last a lifetime. Don't miss out on this
                amazing opportunity!
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl mb-6">Your Information</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label
                htmlFor="name"
                className="block text-sm mb-2 text-gray-700"
              >
                Full Name *
              </label>
              <input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="John Doe"
                required
              />
            </div>

            <div>
              <label
                htmlFor="email"
                className="block text-sm mb-2 text-gray-700"
              >
                Email Address *
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="john@example.com"
                required
              />
            </div>

            <div>
              <label
                htmlFor="phone"
                className="block text-sm mb-2 text-gray-700"
              >
                Phone Number *
              </label>
              <input
                id="phone"
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="+1 (555) 123-4567"
                required
              />
            </div>

            <button
              type="submit"
              className="w-full bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 transition-colors"
            >
              Continue to Seat Selection
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
