import { useNavigate } from 'react-router-dom';
import { useBooking } from '../context/BookingContext';
import { useState } from 'react';

const ROWS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
const SEATS_PER_ROW = 10;

export function SeatPage() {
  const navigate = useNavigate();
  const { selectedEvent, selectedSeats, setSelectedSeats, userInfo } = useBooking();
  const [bookedSeats] = useState<string[]>([
    'A3',
    'A4',
    'B5',
    'C2',
    'C7',
    'D8',
    'E4',
    'F6',
  ]);

  if (!selectedEvent || !userInfo) {
    navigate('/home');
    return null;
  }

  const toggleSeat = (seatId: string) => {
    if (bookedSeats.includes(seatId)) return;

    setSelectedSeats(
      selectedSeats.includes(seatId)
        ? selectedSeats.filter((s) => s !== seatId)
        : [...selectedSeats, seatId]
    );
  };

  const getSeatStatus = (seatId: string) => {
    if (bookedSeats.includes(seatId)) return 'booked';
    if (selectedSeats.includes(seatId)) return 'selected';
    return 'available';
  };

  const totalPrice = selectedSeats.length * selectedEvent.price;

  const handleContinue = () => {
    if (selectedSeats.length === 0) {
      alert('Please select at least one seat');
      return;
    }
    navigate('/payment');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl text-purple-600">Ticket Booking</h1>
          <button
            onClick={() => navigate(-1)}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
          >
            ← Back
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <h2 className="text-2xl mb-2">Select Your Seats</h2>
          <p className="text-gray-600">{selectedEvent.title}</p>
        </div>

        {/* Legend */}
        <div className="flex gap-6 justify-center mb-8">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-green-500 rounded"></div>
            <span className="text-sm">Available</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-purple-600 rounded"></div>
            <span className="text-sm">Selected</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-gray-400 rounded"></div>
            <span className="text-sm">Booked</span>
          </div>
        </div>

        {/* Screen */}
        <div className="bg-gradient-to-b from-gray-300 to-gray-200 rounded-lg p-4 mb-8 text-center">
          <p className="text-sm text-gray-600">SCREEN</p>
        </div>

        {/* Seats */}
        <div className="bg-white p-8 rounded-lg shadow-md mb-6">
          <div className="space-y-4">
            {ROWS.map((row) => (
              <div key={row} className="flex items-center gap-2 justify-center">
                <span className="w-8 text-center">{row}</span>
                <div className="flex gap-2">
                  {Array.from({ length: SEATS_PER_ROW }, (_, i) => {
                    const seatId = `${row}${i + 1}`;
                    const status = getSeatStatus(seatId);
                    return (
                      <button
                        key={seatId}
                        onClick={() => toggleSeat(seatId)}
                        disabled={status === 'booked'}
                        className={`w-8 h-8 rounded text-xs transition-colors ${
                          status === 'available'
                            ? 'bg-green-500 hover:bg-green-600 text-white'
                            : status === 'selected'
                            ? 'bg-purple-600 text-white'
                            : 'bg-gray-400 text-gray-200 cursor-not-allowed'
                        }`}
                        title={seatId}
                      >
                        {i + 1}
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Summary */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <div className="flex justify-between items-center mb-4">
            <div>
              <p className="text-sm text-gray-600">Selected Seats</p>
              <p className="text-lg">
                {selectedSeats.length > 0 ? selectedSeats.join(', ') : 'None'}
              </p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-600">Total Price</p>
              <p className="text-2xl text-purple-600">${totalPrice}</p>
            </div>
          </div>
          <button
            onClick={handleContinue}
            disabled={selectedSeats.length === 0}
            className="w-full bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            Continue to Payment
          </button>
        </div>
      </main>
    </div>
  );
}
