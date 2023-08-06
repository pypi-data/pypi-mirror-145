/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2022, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////
import PropTypes from 'prop-types';
import BaseUISchema from 'sources/SchemaView/base_schema.ui';

/* Common Prop types */
const CustomPropTypes = {
  ref: PropTypes.oneOfType([
    PropTypes.func,
    PropTypes.shape({ current: PropTypes.instanceOf(Element) }),
    PropTypes.object
  ]),

  schemaUI: PropTypes.instanceOf(BaseUISchema),

  children: PropTypes.oneOfType([
    PropTypes.arrayOf(PropTypes.node),
    PropTypes.node,
  ]),

  className: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.object,
    PropTypes.array,
  ]),

  shortcut: PropTypes.shape({
    alt: PropTypes.bool,
    control: PropTypes.bool,
    shift: PropTypes.bool,
    key: PropTypes.shape({
      char: PropTypes.string,
    }),
  }),
};

export default CustomPropTypes;
