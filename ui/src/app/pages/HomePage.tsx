import { useNavigate } from "react-router-dom";
import { useBooking, Event } from "../context/BookingContext";
import { useState } from "react";
import { Search } from "lucide-react";

const MOCK_EVENTS: Event[] = [
  {
    id: "1",
    title: "Rock Concert 2026",
    date: "2026-02-15",
    time: "19:00",
    venue: "Madison Square Garden",
    price: 85,
    category: "Music",
    image:
      "https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?w=800&h=600&fit=crop",
  },
  {
    id: "2",
    title: "Comedy Night Live",
    date: "2026-02-20",
    time: "20:00",
    venue: "The Comedy Store",
    price: 45,
    category: "Comedy",
    image:
      "https://images.unsplash.com/photo-1585699324551-f6c309eedeca?w=800&h=600&fit=crop",
  },
  {
    id: "3",
    title: "Broadway Musical",
    date: "2026-03-01",
    time: "18:30",
    venue: "Broadway Theatre",
    price: 120,
    category: "Theatre",
    image:
      "https://images.unsplash.com/photo-1503095396549-807759245b35?w=800&h=600&fit=crop",
  },
  {
    id: "4",
    title: "Sports Championship",
    date: "2026-03-10",
    time: "17:00",
    venue: "Sports Arena",
    price: 95,
    category: "Sports",
    image:
      "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800&h=600&fit=crop",
  },
  {
    id: "5",
    title: "Jazz Festival",
    date: "2026-03-15",
    time: "19:30",
    venue: "Blue Note Jazz Club",
    price: 65,
    category: "Music",
    image:
      "https://images.unsplash.com/photo-1415201364774-f6f0bb35f28f?w=800&h=600&fit=crop",
  },
  {
    id: "6",
    title: "Art Exhibition",
    date: "2026-03-20",
    time: "10:00",
    venue: "Metropolitan Museum",
    price: 30,
    category: "Art",
    image:
      "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=800&h=600&fit=crop",
  },
];

export function HomePage() {
  const navigate = useNavigate();
  const { setSelectedEvent, loggedInUser, setLoggedInUser } = useBooking();
  const [searchQuery, setSearchQuery] = useState("");

  const handleEventClick = (event: Event) => {
    setSelectedEvent(event);
    navigate("/info");
  };

  const handleLogout = () => {
    setLoggedInUser(null);
    navigate("/");
  };

  // Filter events based on search query
  const filteredEvents = MOCK_EVENTS.filter((event) => {
    const query = searchQuery.toLowerCase();
    return (
      event.title.toLowerCase().includes(query) ||
      event.category.toLowerCase().includes(query) ||
      event.venue.toLowerCase().includes(query)
    );
  });

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl text-purple-600">Ticket Booking</h1>
          <div className="flex items-center gap-4">
            {loggedInUser && (
              <span className="text-sm text-gray-600">
                Welcome,{" "}
                <span className="font-medium text-gray-900">
                  {loggedInUser}
                </span>
              </span>
            )}
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-3xl mb-2">Upcoming Events</h2>
          <p className="text-gray-600">
            Find and book tickets for amazing events
          </p>
        </div>

        {/* Search Bar */}
        <div className="mb-6 relative">
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Search by event, category, or venue..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery("")}
              className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          )}
        </div>

        {/* Results count */}
        {searchQuery && (
          <div className="mb-4 text-sm text-gray-600">
            Found {filteredEvents.length}{" "}
            {filteredEvents.length === 1 ? "event" : "events"}
          </div>
        )}

        {/* Events Grid */}
        {filteredEvents.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">
              No events found matching your search.
            </p>
            <button
              onClick={() => setSearchQuery("")}
              className="mt-4 text-purple-600 hover:text-purple-700"
            >
              Clear search
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredEvents.map((event) => (
              <div
                key={event.id}
                onClick={() => handleEventClick(event)}
                className="bg-white rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow cursor-pointer"
              >
                <img
                  src={event.image}
                  alt={event.title}
                  className="w-full h-48 object-cover"
                />
                <div className="p-5">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs px-2 py-1 bg-purple-100 text-purple-700 rounded">
                      {event.category}
                    </span>
                    <span className="text-purple-600">${event.price}</span>
                  </div>
                  <h3 className="text-xl mb-2">{event.title}</h3>
                  <div className="text-sm text-gray-600 space-y-1">
                    <p>📅 {new Date(event.date).toLocaleDateString()}</p>
                    <p>🕐 {event.time}</p>
                    <p>📍 {event.venue}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
