export declare class Point {
    readonly x: number;
    readonly y: number;
    constructor(x: number, y: number);
    translate(offset: Point, size: number): Point;
    add(other: Point): Point;
    mod(size: number): Point;
    /**
     * Gets the manhatten distance between two points
     */
    distanceTo(other: Point, size: number): number;
    /**
     * Converts a 2d position in the form (x, y) to an index in the observation.kore list.
     * See fromIndex for the inverse.
     */
    toIndex(size: number): number;
    static fromIndex(index: number, size: number): Point;
    abs(): Point;
    equals(other: Point): boolean;
    toString(): string;
    multiply(factor: number): Point;
    subtract(other: Point): Point;
}
