import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { BookingProvider } from "./context/BookingContext";
import { LoginPage } from "./pages/LoginPage";
import { HomePage } from "./pages/HomePage";
import { InfoPage } from "./pages/InfoPage";
import { SeatPage } from "./pages/SeatPage";
import { PaymentPage } from "./pages/PaymentPage";

export default function App() {
  return (
    <BrowserRouter>
      <BookingProvider>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/info/:showId" element={<InfoPage />} />
          <Route path="/seat" element={<SeatPage />} />
          <Route path="/payment" element={<PaymentPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BookingProvider>
    </BrowserRouter>
  );
}
