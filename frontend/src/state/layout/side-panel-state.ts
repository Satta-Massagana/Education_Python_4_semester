
import { create } from 'zustand';

export interface PanelState {
  isOpen: boolean;
  setIsOpen: (value: boolean) => void;
  close: () => void;
}

export const useSidePanelStore = create<PanelState>()(
    (set) => ({
      isOpen: true,
      setIsOpen: (value: boolean) => set(() => ({ isOpen: value })),
      close: () => set(() => ({ isOpen: false }))
    })
);
