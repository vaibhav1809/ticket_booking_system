import { useNavigate } from "react-router-dom";
import { useBooking, Event, Event2 } from "../context/BookingContext";
import { useCallback, useEffect, useState } from "react";
import { Search } from "lucide-react";
import { fetchShows } from "../utils/api";

const DEFAULT_CATEGORY = "all";
const DEFAULT_CITY = "Bangalore";
const getEventImagePath = (eventId: string) => {
  return `/${eventId}.jpg`;
};

export function HomePage() {
  const navigate = useNavigate();
  const { setSelectedEvent, loggedInUser, setLoggedInUser } = useBooking();
  const [searchQuery, setSearchQuery] = useState("");
  const [events, setEvents] = useState<Event2[]>([]);

  const fetchData = useCallback(async () => {
    try {
      const shows: Event2[] = await fetchShows({
        category: DEFAULT_CATEGORY,
        city: DEFAULT_CITY,
        token: loggedInUser ?? "demo-user",
      });
      setEvents(shows);
    } catch (error) {
      console.error("Failed to load shows", error);
    }
  }, [loggedInUser]);

  useEffect(() => {
    void fetchData();
  }, [fetchData]);

  const mapShowToSelectedEvent = (show: Event2): Event => {
    const startTime = new Date(show.start_time);
    const time = startTime.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    return {
      id: String(show.show_id),
      title: show.title,
      date: startTime.toISOString(),
      time,
      venue: show.venue_name,
      price: show.min_price,
      category: show.category,
      image: getEventImagePath(show.event_id.toString()),
    };
  };

  const handleEventClick = (event: Event2) => {
    setSelectedEvent(mapShowToSelectedEvent(event));
    navigate(`/info/${event.show_id}`);
  };

  const handleLogout = () => {
    setLoggedInUser(null);
    navigate("/");
  };

  // Filter events based on search query
  const filteredEvents = events.filter((event) => {
    const query = searchQuery.toLowerCase();
    return (
      event.title.toLowerCase().includes(query) ||
      event.category.toLowerCase().includes(query) ||
      event.venue_name.toLowerCase().includes(query)
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
                key={event.show_id}
                onClick={() => handleEventClick(event)}
                className="bg-white rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow cursor-pointer"
              >
                <img
                  src={getEventImagePath(event.event_id.toString())}
                  alt={event.title}
                  className="w-full h-48 object-cover"
                />
                <div className="p-5">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs px-2 py-1 bg-purple-100 text-purple-700 rounded">
                      {event.category}
                    </span>
                    <span className="text-purple-600">
                      {event.currency} {event.min_price}
                    </span>
                  </div>
                  <h3 className="text-xl mb-2">{event.title}</h3>
                  <div className="text-sm text-gray-600 space-y-1">
                    <p>{new Date(event.start_time).toDateString()}</p>
                    <p>
                      {new Date(event.start_time).toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </p>
                    <p>{event.venue_name}</p>
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
