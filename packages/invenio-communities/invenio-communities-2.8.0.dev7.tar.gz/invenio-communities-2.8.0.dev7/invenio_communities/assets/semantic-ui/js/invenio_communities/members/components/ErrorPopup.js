/*
 * This file is part of Invenio.
 * Copyright (C) 2022 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import React from "react";
import { Label, Popup } from "semantic-ui-react";
import PropTypes from "prop-types";

export const ErrorPopup = ({ trigger, error, onClose }) => {
  if (!error) {
    return null;
  }

  return (
    <Popup
      basic
      className="p-0 borderless shadowless mb-1"
      open={!!error}
      position="top center"
      content={
        <Label
          content={error}
          basic
          className="mb-5 error"
          pointing="below"
          removeIcon="close"
          onRemove={onClose}
        />
      }
      trigger={trigger}
    />
  );
};

ErrorPopup.propTypes = {
  trigger: PropTypes.node.isRequired,
  error: PropTypes.string,
  onClose: PropTypes.func.isRequired,
};

ErrorPopup.defaultProps = {
  error: "",
};
