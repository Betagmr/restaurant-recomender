import asyncio
import re
import time
from typing import Any

import pandas as pd
from playwright.async_api import ElementHandle, Page, async_playwright
from tqdm import tqdm


def get_zone_url(zone: str) -> str:
    base_url = f"https://www.google.com/search?q=bares+y+restaurantes+bilbao+{zone}"
    site_url = (
        "&uds=AMwkrPv4b_4cYRjioaEQc4CO9do7Uwi_qVOE8vzTSEbjWaJqe_OdBFIUriiQ76J"
        "C9goO_6Bx5llttfasDMCpy0gSYR6-XrEKD9DJEJUU3WEPxZa7Gn-Iu4A3f6H61I2ZIL5Wy"
        "L3yJBLXCFix-ukO6c1PbOlN_mSAvg&udm=1&sa=X&ved=2ahUKEwjA64Pj1cmEAxW70wIHH"
        "f0BDl0Qs6gLegQICxAB&biw=1280&bih=720#vhid=/g/1td66mxk&vssid=rllrl&ip=1"
    )

    return base_url + site_url


async def get_normalize_content(element: ElementHandle) -> str:
    if element is None:
        return None

    element_content = await element.inner_text()

    return (
        element_content.replace(",", "")
        .replace("(", "")
        .replace(")", "")
        .replace("\xa0", "")
        .replace("mil", "000")
        .replace("\u2066", "")
        .replace("\u2069", "")
    )


def get_hours_to_dict(hours: str | None) -> dict[str, str]:
    if hours is None:
        return {}

    labels = [label.split("\n")[-1] for label in hours.split("\t")[:-1]]
    hours_list = re.split(rf"(?:{'|'.join(labels)})\t", hours)[1:]

    return dict(
        [
            [label, element.strip().split("\n")]
            for label, element in zip(labels, hours_list)
        ]
    )


async def get_element_content(page: Page, element: ElementHandle) -> dict[str, Any]:
    # Getting card content
    title = await element.query_selector("span.OSrXXb.e62wic")
    await title.click()

    time.sleep(0.85)
    # input()
    show_more = await element.query_selector("div[jsname='fsEqyc']")
    show_hours = await page.query_selector("div.LmBKnf")

    if show_hours:
        await show_hours.click()
        opening_hours = await (await page.query_selector("div.aNF4pc")).inner_text()
    else:
        opening_hours = None

    if show_more:
        await show_more.click()

    # Getting card details
    stars_avg = await element.query_selector("span.yi40Hd.YrbPuc")
    n_reviews = await element.query_selector("span.RDApEe.YrbPuc")
    price_range = await element.query_selector("div:nth-child(2) > span:nth-child(2)")
    description = await page.query_selector("c-wiz[jsrenderer='Gdjwac']")
    facilities = await page.query_selector("div.fgzP8e")
    street = await page.query_selector("div.F2yIXb")
    phone_number = await page.query_selector("div.eigqqc")
    featured_reviews = await page.query_selector_all("span.Vz1Vkc")
    extra_content = await page.query_selector_all(
        "div.cg9Tke-KZWGte-ezkdbf-BXzADf."
        "cg9Tke-KZWGte-ezkdbf-pTTvpb-lvvS4b."
        "nNzjpf-twKXnc-V67aGc-ACwpOe-CZjX4e."
        "nNzjpf-twKXnc-V67aGc-fKRGO."
        "nNzjpf-twKXnc-V67aGc-taAgAb-lvvS4b"
    )

    return {
        "title": await get_normalize_content(title),
        "description": await get_normalize_content(description),
        "n_reviews": await get_normalize_content(n_reviews),
        "stars_avg": await stars_avg.inner_text(),
        "price_range": await get_normalize_content(price_range),
        "facilities": await get_normalize_content(facilities),
        "street": await street.inner_text() if street else "",
        "opening_hours": get_hours_to_dict(opening_hours),
        "phone_number": await get_normalize_content(phone_number),
        "featured_reviews": [await review.inner_text() for review in featured_reviews],
        "extra_content": [await get_normalize_content(cont) for cont in extra_content],
    }


async def get_page_position(page: Page) -> int:
    return await page.evaluate("window.innerHeight + window.scrollY")


async def get_all_restaurants(page: Page) -> list[ElementHandle]:
    previous_len = 0
    current_len = await get_page_position(page)

    while current_len != previous_len:
        await page.mouse.wheel(0, 10000)
        show_more = await page.query_selector("div.WZH4jc.w7LJsc")

        if show_more:
            await show_more.click()

        previous_len = current_len
        current_len = await get_page_position(page)

        time.sleep(1.5)

    return await page.query_selector_all("div.rllt__details")


async def main(zone_list: list[str]) -> None:
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=False)
    page = await browser.new_page()

    await page.goto("https://www.google.com")

    # Accepting cookies
    accept_button = await page.wait_for_selector("button#L2AGLb")
    await accept_button.click()

    # Searching for restaurants
    for zone in zone_list:
        await page.goto(get_zone_url(zone))
        list_of_restaurants = await get_all_restaurants(page)

        restaurant_content = []
        for restaurant in tqdm(list_of_restaurants, total=len(list_of_restaurants)):
            try:
                content = await get_element_content(page, restaurant)
            except Exception:
                continue

            restaurant_content.append(content)

        content_df = pd.DataFrame(restaurant_content)
        data_url = f"./data/raw/{zone}_data.csv"
        content_df.to_csv(data_url, index=False)


if __name__ == "__main__":
    list_of_zones = []

    if list_of_zones:
        asyncio.run(main(list_of_zones))
