{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a5cf8dcd-cf9d-48b4-928a-6135dd70e135",
   "metadata": {},
   "outputs": [],
   "source": [
    "from test_cases import requests\n",
    "def reactive_agent(request):\n",
    "    # Rule 1: Check inventory\n",
    "    if request[\"inventory\"] < request[\"quantity\"]:\n",
    "        return \"Insufficient Inventory. Please wait for restocking.\"\n",
    "    # Rule 2: High-priority requests\n",
    "    if request[\"priority\"] == \"High\":\n",
    "        if request[\"vehicle\"]:\n",
    "            return \"Deliver Immediately\"\n",
    "        return \"High Priority - Waiting for Vehicle\"\n",
    "    # Rule 3: Medium-priority requests\n",
    "    if request[\"priority\"] == \"Medium\":\n",
    "        if request[\"vehicle\"]:\n",
    "            return \"Deliver\"\n",
    "        return \"Medium Priority - Please wait for vehicle.\"\n",
    "\n",
    "    # Rule 4: Low-priority requests\n",
    "    if request[\"priority\"] == \"Low\":\n",
    "        return \"Wait for Scheduled Delivery\"\n",
    "    # Rule 5: Unknown priority\n",
    "    return \"Invalid Request\"\n",
    "for request in requests:\n",
    "    print(request)\n",
    "    print(\"Decision:\", reactive_agent(request))\n",
    "    print(\"=\" * 60)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
