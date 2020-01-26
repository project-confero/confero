import React from "react";
import { Box, Button } from "@material-ui/core";

interface FilterOption {
  value: string;
  label: string;
}

export interface FilterButtonsProps {
  value: string[];
  options: FilterOption[];
  onChange: (values: string[]) => void;
}

const FilterButtons: React.FunctionComponent<FilterButtonsProps> = ({
  value: filters,
  options,
  onChange
}) => {
  const onClick = (value: string) => {
    if (filters.includes(value)) {
      onChange(filters.filter(filter => filter !== value));
    } else {
      onChange([...filters, value]);
    }
  };

  return (
    <Box display="flex" my={2}>
      {options.map(({ value, label }) => (
        <Box key={value} mr={2}>
          <Button
            variant="contained"
            onClick={() => onClick(value)}
            color={filters.includes(value) ? "primary" : "default"}
          >
            {label}
          </Button>
        </Box>
      ))}
    </Box>
  );
};

export default FilterButtons;
