import { useCallback, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { useBooking, ShowDetails } from "../context/BookingContext";
import { fetchShowDetails } from "../utils/api";

export function InfoPage() {
  const navigate = useNavigate();
  const { showId } = useParams();
  const { selectedEvent, setUserInfo, loggedInUser } = useBooking();
  
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  
  const [showDetails, setShowDetails] = useState<ShowDetails | null>(null);

  const getEventImagePath = (eventId: number) => {
    return `/${eventId}.jpg`;
  };

  const fetchData = useCallback(async () => {
    if (!showId) {
      navigate("/home");
      return;
    }

    setIsLoading(true);
    setLoadError(null);

    try {
      const details = await fetchShowDetails({
        showId,
        token: loggedInUser ?? "demo-user",
      });
      setShowDetails(details);
    } catch (error) {
      console.error("Failed to load show details", error);
      setLoadError("Unable to load event details right now.");
    } finally {
      setIsLoading(false);
    }
  }, [showId, loggedInUser, navigate]);

  useEffect(() => {
    void fetchData();
  }, [fetchData]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setUserInfo({ name, email, phone });
    navigate("/seat");
  };

  const selectedEventPrice =
    (selectedEvent as { price?: number; min_price?: number } | null)?.price ??
    (selectedEvent as { min_price?: number } | null)?.min_price;
  const selectedEventCurrency =
    (selectedEvent as { currency?: string } | null)?.currency ?? "INR";

  const content = () => {
    if (!showDetails) {
      const message =
        isLoading && !loadError
          ? "Loading event details..."
          : loadError || "Event details not available.";

      return (
        <div className="bg-white rounded-lg shadow-md p-6 text-center text-gray-600">
          {message}
        </div>
      );
    }

    const startTime = new Date(showDetails.start_time);
    const timeLabel = startTime.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    return (
      <>
        <div className="bg-white rounded-lg shadow-md overflow-hidden mb-8">
          <img
            src={getEventImagePath(showDetails.event_id)}
            alt={showDetails.title}
            className="w-full h-64 object-cover"
          />
          <div className="p-6">
            <div className="mb-4">
              <span className="text-xs px-3 py-1 bg-purple-100 text-purple-700 rounded">
                {showDetails.category}
              </span>
            </div>
            <h2 className="text-3xl mb-4">{showDetails.title}</h2>
            <div className="grid grid-cols-2 gap-4 text-gray-700 mb-6">
              <div>
                <p className="text-sm text-gray-500 mb-1">Date</p>
                <p>{startTime.toLocaleDateString()}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500 mb-1">Time</p>
                <p>{timeLabel}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500 mb-1">Venue</p>
                <p>{showDetails.venue_name}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500 mb-1">Price</p>
                <p className="text-purple-600">
                  {selectedEventPrice !== undefined
                    ? `${selectedEventCurrency} ${selectedEventPrice}`
                    : "Pricing unavailable"}
                </p>
              </div>
            </div>
            <div className="border-t pt-4">
              <h3 className="mb-2">About This Event</h3>
              <p className="text-gray-600 text-sm">
                Join us for an unforgettable experience at {showDetails.title}.
                This event promises to deliver entertainment, excitement, and
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
      </>
    );
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
        {content()}
      </main>
    </div>
  );
}
