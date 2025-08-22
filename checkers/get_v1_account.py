from datetime import datetime

from hamcrest import assert_that, has_property, ends_with, instance_of, has_properties, greater_than_or_equal_to, \
    equal_to


class GetV1Account:

    @classmethod
    def get_v1_account(
            cls,
            response
    ):
        assert_that(response, has_property('resource', has_property('login', ends_with('Roman'))))
        assert_that(response, has_property('resource', has_property('info', '')))
        assert_that(response, has_property('resource', has_property('registration', instance_of(datetime))))
        assert_that(response, has_property('resource', has_properties(
            {'settings': has_properties({
                'paging': has_properties({

                    "posts_per_page": greater_than_or_equal_to(10),
                    "comments_per_page": equal_to(10),
                    "topics_per_page": equal_to(10),
                    "messages_per_page": equal_to(10),
                    "entities_per_page": equal_to(10)
                })
            })}
        )))

