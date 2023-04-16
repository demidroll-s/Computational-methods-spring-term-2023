#pragma once

class Priceable {
public:
    virtual double Price() const = 0;
};