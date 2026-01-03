import { useNavigate } from 'react-router-dom';
import { useBooking } from '../context/BookingContext';
import { useState } from 'react';

export function PaymentPage() {
  const navigate = useNavigate();
  const { selectedEvent, selectedSeats, userInfo } = useBooking();
  const [cardNumber, setCardNumber] = useState('');
  const [cardName, setCardName] = useState('');
  const [expiryDate, setExpiryDate] = useState('');
  const [cvv, setCvv] = useState('');
  const [showSuccess, setShowSuccess] = useState(false);

  if (!selectedEvent || !userInfo || selectedSeats.length === 0) {
    navigate('/home');
    return null;
  }

  const totalPrice = selectedSeats.length * selectedEvent.price;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setShowSuccess(true);
    // Mock payment success - navigate to home after 3 seconds
    setTimeout(() => {
      navigate('/home');
    }, 3000);
  };

  if (showSuccess) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-xl max-w-md text-center">
          <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg
              className="w-8 h-8 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
          <h2 className="text-2xl mb-2">Booking Confirmed!</h2>
          <p className="text-gray-600 mb-4">
            Your tickets have been successfully booked. A confirmation email has been sent to{' '}
            {userInfo.email}
          </p>
          <div className="bg-gray-50 p-4 rounded-lg text-left space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">Event:</span>
              <span>{selectedEvent.title}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Seats:</span>
              <span>{selectedSeats.join(', ')}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Total:</span>
              <span className="text-purple-600">${totalPrice}</span>
            </div>
          </div>
          <p className="text-sm text-gray-500 mt-4">Redirecting to home...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl text-purple-600">Ticket Booking</h1>
          <button
            onClick={() => navigate('/seat')}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
          >
            ← Back
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h2 className="text-2xl mb-6">Payment Details</h2>

        <div className="grid md:grid-cols-3 gap-6">
          {/* Payment Form */}
          <div className="md:col-span-2">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="mb-6">Card Information</h3>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label htmlFor="cardNumber" className="block text-sm mb-2 text-gray-700">
                    Card Number *
                  </label>
                  <input
                    id="cardNumber"
                    type="text"
                    value={cardNumber}
                    onChange={(e) => setCardNumber(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                    placeholder="1234 5678 9012 3456"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="cardName" className="block text-sm mb-2 text-gray-700">
                    Cardholder Name *
                  </label>
                  <input
                    id="cardName"
                    type="text"
                    value={cardName}
                    onChange={(e) => setCardName(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                    placeholder="John Doe"
                    required
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="expiryDate" className="block text-sm mb-2 text-gray-700">
                      Expiry Date *
                    </label>
                    <input
                      id="expiryDate"
                      type="text"
                      value={expiryDate}
                      onChange={(e) => setExpiryDate(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                      placeholder="MM/YY"
                      required
                    />
                  </div>
                  <div>
                    <label htmlFor="cvv" className="block text-sm mb-2 text-gray-700">
                      CVV *
                    </label>
                    <input
                      id="cvv"
                      type="text"
                      value={cvv}
                      onChange={(e) => setCvv(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                      placeholder="123"
                      maxLength={3}
                      required
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  className="w-full bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 transition-colors"
                >
                  Pay ${totalPrice}
                </button>

                <p className="text-xs text-center text-gray-500">
                  This is a demo payment form. No actual charges will be made.
                </p>
              </form>
            </div>
          </div>

          {/* Order Summary */}
          <div className="md:col-span-1">
            <div className="bg-white p-6 rounded-lg shadow-md sticky top-8">
              <h3 className="mb-4">Order Summary</h3>
              <div className="space-y-3 text-sm">
                <div>
                  <p className="text-gray-600 mb-1">Event</p>
                  <p>{selectedEvent.title}</p>
                </div>
                <div>
                  <p className="text-gray-600 mb-1">Date & Time</p>
                  <p>
                    {new Date(selectedEvent.date).toLocaleDateString()} at {selectedEvent.time}
                  </p>
                </div>
                <div>
                  <p className="text-gray-600 mb-1">Venue</p>
                  <p>{selectedEvent.venue}</p>
                </div>
                <div>
                  <p className="text-gray-600 mb-1">Seats</p>
                  <p>{selectedSeats.join(', ')}</p>
                </div>
                <div className="border-t pt-3">
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-600">
                      Price ({selectedSeats.length} {selectedSeats.length === 1 ? 'ticket' : 'tickets'})
                    </span>
                    <span>${selectedEvent.price * selectedSeats.length}</span>
                  </div>
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-600">Service Fee</span>
                    <span>$0</span>
                  </div>
                  <div className="flex justify-between border-t pt-2">
                    <span>Total</span>
                    <span className="text-purple-600 text-lg">${totalPrice}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
