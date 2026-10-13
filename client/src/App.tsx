import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';

type Car = { id: number; [key: string]: any };

type CarContextType = {
  cars: Car[];
  favorites: Car[];
  searchQuery: string;
  setSearchQuery: React.Dispatch<React.SetStateAction<string>>;
  addCar: (newCar: Car) => void;
  toggleFavorite: (car: Car) => void;
  isFavorite: (carId: number) => boolean;
};

const CarContext = createContext<CarContextType | undefined>(undefined);

const FAVORITES_KEY = 'carpoint_favorites';

export const CarProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [cars, setCars] = useState<Car[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>('');

  // Завантаження обраного з localStorage
  const [favorites, setFavorites] = useState<Car[]>(() => {
    const saved = localStorage.getItem(FAVORITES_KEY);
    return saved ? JSON.parse(saved) : [];
  });

  // Автоматичне збереження у localStorage при зміні favorites
  useEffect(() => {
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites));
  }, [favorites]);

  const addCar = (newCar: Car) => {
    setCars((prev) => [newCar, ...prev]);
  };

  const toggleFavorite = (car: Car) => {
    setFavorites((prev) => {
      const exists = prev.some((item) => item.id === car.id);
      if (exists) {
        return prev.filter((item) => item.id !== car.id);
      }
      return [...prev, car];
    });
  };

  const isFavorite = (carId: number) => {
    return favorites.some((car) => car.id === carId);
  };

  return (
    <CarContext.Provider
      value={{
        cars,
        favorites,
        searchQuery,
        setSearchQuery,
        addCar,
        toggleFavorite,
        isFavorite,
      }}
    >
      {children}
    </CarContext.Provider>
  );
};

export const useCarContext = (): CarContextType => {
  const context = useContext(CarContext);
  if (!context) {
    throw new Error('useCarContext must be used within a CarProvider');
  }
  return context;
};