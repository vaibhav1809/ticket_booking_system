import React, { createContext, useContext, useState, ReactNode } from "react";

export interface Event {
  id: string;
  title: string;
  date: string;
  time: string;
  venue: string;
  price: number;
  category: string;
  image: string;
}

export interface Event2 {
  show_id: number;
  event_id: number;
  image: string | undefined;
  category: string;
  title: string;
  start_time: string;
  end_time: string;
  venue_name: string;
  city: string;
  min_price: number;
  currency: string;
}

export interface ShowDetails {
  show_id: number;
  start_time: string;
  end_time: string;
  status: string;
  event_id: number;
  category: string;
  title: string;
  duration_min: number;
  language: string;
  genre: string;
  venue_id: number;
  venue_name: string;
  location: string;
  city: string;
  country: string;
  pincode: string;
  address: string;
}

interface BookingContextType {
  selectedEvent: Event | null;
  setSelectedEvent: (event: Event | null) => void;
  selectedSeats: string[];
  setSelectedSeats: (seats: string[]) => void;
  userInfo: {
    name: string;
    email: string;
    phone: string;
  } | null;
  setUserInfo: (
    info: { name: string; email: string; phone: string } | null
  ) => void;
  loggedInUser: string | null;
  setLoggedInUser: (user: string | null) => void;
}

const BookingContext = createContext<BookingContextType | undefined>(undefined);

export function BookingProvider({ children }: { children: ReactNode }) {
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [selectedSeats, setSelectedSeats] = useState<string[]>([]);
  const [userInfo, setUserInfo] = useState<{
    name: string;
    email: string;
    phone: string;
  } | null>(null);
  const [loggedInUser, setLoggedInUser] = useState<string | null>(null);

  return (
    <BookingContext.Provider
      value={{
        selectedEvent,
        setSelectedEvent,
        selectedSeats,
        setSelectedSeats,
        userInfo,
        setUserInfo,
        loggedInUser,
        setLoggedInUser,
      }}
    >
      {children}
    </BookingContext.Provider>
  );
}

export function useBooking() {
  const context = useContext(BookingContext);
  if (context === undefined) {
    throw new Error("useBooking must be used within a BookingProvider");
  }
  return context;
}
