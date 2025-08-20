from datetime import datetime

from hamcrest import assert_that, has_property, ends_with, all_of, instance_of, has_properties, equal_to, \
    greater_than_or_equal_to, greater_than


def test_get_v1_account_auth(
        auth_account_helper
):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    assert_that(response, has_property('resource', has_property('login', ends_with('Roman'))))
    assert_that(response, has_property('resource', has_property('info', '')))
    assert_that(response,has_property('resource', has_property('registration', instance_of(datetime))))

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
    print(response)


def test_get_v1_account_no_auth(
        account_helper
):
    account_helper.dm_account_api.account_api.get_v1_account()
