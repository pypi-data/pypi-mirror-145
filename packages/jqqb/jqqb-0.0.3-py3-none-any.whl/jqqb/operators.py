class Operators:

    # left = The property of the object being evaluated.
    # right = The value that was entered/selected by the user
    # from the frontend (rule `value` property)

    @staticmethod
    def eval_begins_with(left, right):
        if isinstance(left, list):
            return any(map(lambda x: x.startswith(right), left))
        return left.startswith(right)

    @staticmethod
    def eval_between(inputs, bounds):
        if inputs is None:
            return False

        return bounds[0] < inputs < bounds[1]

    @staticmethod
    def eval_contains(left, right):
        if isinstance(right, list):
            if isinstance(left, list):
                return any([any(map(lambda x: r in x, left)) for r in right])
            return any([r == left for r in right])
        else:
            if isinstance(left, list):
                return any(map(lambda x: right in x, left))
            return right in left

    @staticmethod
    def eval_ends_with(left, right):
        if isinstance(left, list):
            return any(map(lambda x: x.endswith(right), left))
        return left.endswith(right)

    @staticmethod
    def eval_equal(left, right):
        if isinstance(left, list):
            return any(map(lambda x: x == right, left))
        return left == right

    @staticmethod
    def eval_greater(left, right):
        if left is None:
            return False

        if isinstance(left, list):
            return any(map(lambda x: x > right, left))
        return left > right

    @staticmethod
    def eval_greater_or_equal(left, right):
        if left is None:
            return False

        if isinstance(left, list):
            return any(map(lambda x: x >= right, left))
        return left >= right

    @staticmethod
    def eval_in(left, right):
        if left is None:
            return False

        if isinstance(left, list):
            return all([_ in right for _ in left])
        return left in right

    @staticmethod
    def eval_is_empty(inputs, _):
        if isinstance(inputs, list):
            return not bool(inputs)
        return not bool(inputs and inputs.strip())

    @staticmethod
    def eval_is_not_empty(inputs, _):
        if isinstance(inputs, list):
            return bool(inputs)
        return bool(inputs and inputs.strip())

    @staticmethod
    def eval_is_not_null(inputs, _):
        return inputs is not None

    @staticmethod
    def eval_is_null(inputs, _):
        return inputs is None

    @staticmethod
    def eval_less(left, right):
        if left is None:
            return False

        if isinstance(left, list):
            return any(map(lambda x: x < right, left))
        return left < right

    @staticmethod
    def eval_less_or_equal(left, right):
        if left is None:
            return False

        if isinstance(left, list):
            return any(map(lambda x: x <= right, left))
        return left <= right

    @staticmethod
    def eval_not_begins_with(left, right):
        if isinstance(left, list):
            return not any(map(lambda x: x.startswith(right), left))
        return not left.startswith(right)

    @staticmethod
    def eval_not_between(inputs, bounds):
        if inputs is None:
            return False

        if isinstance(inputs, list):
            return not any(
                map(lambda x: x <= bounds[0] or x >= bounds[1], inputs)
            )
        return inputs <= bounds[0] or inputs >= bounds[1]

    @staticmethod
    def eval_not_contains(left, right):
        if isinstance(right, list):
            if isinstance(left, list):
                return not any(
                    [any(map(lambda x: r in x, left)) for r in right]
                )
            return not any([r == left for r in right])
        else:
            if isinstance(left, list):
                return not any(map(lambda x: right in x, left))
            return right not in left

    @staticmethod
    def eval_not_ends_with(left, right):
        if isinstance(left, list):
            return not any(map(lambda x: x.endswith(right), left))
        return not left.endswith(right)

    @staticmethod
    def eval_not_equal(left, right):
        if isinstance(left, list):
            return not any(map(lambda x: x == right, left))
        return left != right

    @staticmethod
    def eval_not_in(left, right):
        if left is None:
            return False

        if isinstance(left, list):
            return not all([_ in right for _ in left])
        return left in right
