
import { FC, MouseEventHandler } from 'react';
import { EtButtonStyle } from './et-button-style';
import './et-button.scss';

export interface EtButtonProps {
  label: string;
  style: EtButtonStyle;
  disabled?: boolean;
  type?: "button" | "submit" | "reset";
  onClick?: MouseEventHandler<HTMLButtonElement>
}

const EtButton: FC<EtButtonProps> = ({
  label,
  style,
  disabled,
  type = 'button',
  onClick
}) => {
  return <button
    className={'et-button et-button_' + style.toString()}
    onClick={ onClick }
    disabled={ disabled }
    type={ type }
  >
      <div className="et-button__body">
        <span className="et-button__label">{ label }</span>
      </div>
  </button>;
}

export default EtButton;
