import React, { createContext, useState, useContext, Dispatch, SetStateAction } from 'react';

type PopupContextType = {
    isPopupVisible: boolean;
    setPopupVisible: Dispatch<SetStateAction<boolean>>;
};

//Provie default values for context
const PopupContext = createContext<PopupContextType>({
    isPopupVisible: false,
    setPopupVisible: () => {}, //empty function as space holder
});

export const usePopup = () => useContext(PopupContext);

export const PopupProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
    const [isPopupVisible, setPopupVisible] = useState(false);

    return (
        <PopupContext.Provider value={{ isPopupVisible, setPopupVisible }}>
            {children}
        </PopupContext.Provider>
    );
};
